import httpx

from app.gateway import ServeGateway, bridge_prompt


def _serve(handler):
    return ServeGateway(
        base_url="http://x:1",
        password="pw",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_prompt_posts_text_and_returns_inbox():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["body"] = request.read().decode()
        return httpx.Response(200, json={"data": {"id": "msg_1", "type": "user"}})

    inbox = _serve(handler).prompt("ses_9", "hola")
    assert seen["path"] == "/api/session/ses_9/prompt"
    assert '"hola"' in seen["body"]
    assert inbox == "msg_1"


def test_interrupt_returns_flag():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/session/ses_9/interrupt"
        return httpx.Response(200, json={"interrupted": True})

    assert _serve(handler).interrupt("ses_9") is True


def test_bridge_streams_new_text_then_done():
    polls = iter([
        [{"role": "user", "text": "hola", "done": True, "tokens": 2}],
        [{"role": "user", "text": "hola", "done": True, "tokens": 2},
         {"role": "assistant", "text": "eco: ho", "done": False, "tokens": 0}],
        [{"role": "user", "text": "hola", "done": True, "tokens": 2},
         {"role": "assistant", "text": "eco: hola", "done": True, "tokens": 9}],
    ])

    class Stub:
        def messages(self, sid):
            return next(polls)

    sent = []
    result = bridge_prompt(Stub(), "ses_9", sent.append, sleep=lambda s: None, max_polls=10)
    assert "".join(m["delta"] for m in sent if "delta" in m) == "eco: hola"
    assert sent[-1]["done"] is True
    assert sent[-1]["tokens"] == 9
    assert result["text"] == "eco: hola"
