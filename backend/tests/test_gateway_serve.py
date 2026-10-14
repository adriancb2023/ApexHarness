import base64

import httpx

from app.gateway import ServeGateway


def _serve(handler):
    return ServeGateway(
        base_url="http://x:1",
        password="pw",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_list_parses_sessions_and_sends_basic_auth():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers["authorization"]
        seen["path"] = request.url.path
        return httpx.Response(
            200,
            json={"data": [
                {"id": "ses_1", "title": "T1",
                 "tokens": {"input": 10, "output": 5, "reasoning": 1, "cache": {"read": 0, "write": 0}},
                 "cost": 0.0, "location": {"directory": "C:/p"}}
            ]},
        )

    sessions = _serve(handler).list_sessions()
    assert seen["path"] == "/api/session"
    assert seen["auth"] == "Basic " + base64.b64encode(b"opencode:pw").decode()
    assert sessions[0]["id"] == "ses_1"
    assert sessions[0]["tokens"] == 16


def test_get_tokens_sums_session():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"data": [
                {"id": "ses_9", "title": "T",
                 "tokens": {"input": 100, "output": 20, "reasoning": 5, "cache": {"read": 7, "write": 8}},
                 "cost": 0.0, "location": {"directory": "C:/p"}}
            ]},
        )

    assert _serve(handler).get_tokens("ses_9") == 125
