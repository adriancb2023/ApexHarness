from fastapi.testclient import TestClient

from app.main import create_app


class StubServe:
    def __init__(self):
        self.interrupted = []
        self.polls = [
            [{"role": "assistant", "text": "hola real", "done": True, "tokens": 30, "created": 9999999999999}],
        ]

    def prompt(self, session_id, text):
        assert session_id == "ses_9"
        return "msg_1"

    def messages(self, session_id):
        return self.polls[0]

    def send(self, content):
        raise AssertionError("en modo real REST debe usar prompt(), no send()")

    def linked_tokens(self, session_id):
        return None

    def list_sessions(self):
        return []

    def interrupt(self, session_id):
        self.interrupted.append(session_id)
        return True


def _linked(c: TestClient, stub: StubServe):
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    return c.post("/api/sessions", json={"project_id": p["id"], "opencode_session_id": "ses_9"}).json()


def test_interrupt_linked_calls_serve():
    stub = StubServe()
    c = TestClient(create_app(gateway_fake=True, gateway=stub))
    s = _linked(c, stub)
    r = c.post(f"/api/sessions/{s['id']}/interrupt").json()
    assert r == {"interrupted": True}
    assert stub.interrupted == ["ses_9"]


def test_interrupt_unlinked_409():
    c = TestClient(create_app(gateway_fake=True))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c.post("/api/sessions", json={"project_id": p["id"]}).json()
    assert c.post(f"/api/sessions/{s['id']}/interrupt").status_code == 409


def test_rest_linked_fluye_a_real():
    stub = StubServe()
    c = TestClient(create_app(gateway_fake=True, gateway=stub))
    s = _linked(c, stub)
    r = c.post(f"/api/sessions/{s['id']}/messages", json={"content": "hola"}).json()
    assert r["reply"] == "hola real" and r["tokens"] == 30 and r["status"] == "done"


def test_rest_unlinked_en_modo_serve_usa_fake():
    c = TestClient(create_app(gateway_fake=False, gateway=StubServe()))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c.post("/api/sessions", json={"project_id": p["id"]}).json()
    r = c.post(f"/api/sessions/{s['id']}/messages", json={"content": "hola"}).json()
    assert r["reply"] == "eco: hola" and r["status"] == "done"


def test_ws_linked_streams_real():
    stub = StubServe()
    c = TestClient(create_app(gateway_fake=True, gateway=stub))
    s = _linked(c, stub)
    with c.websocket_connect(f"/ws/sessions/{s['id']}") as ws:
        ws.send_json({"content": "hola"})
        got = [ws.receive_json(), ws.receive_json()]
    assert got[0] == {"delta": "hola real"}
    assert got[1]["done"] is True and got[1]["tokens"] == 30

    h = c.get(f"/api/sessions/{s['id']}/messages").json()
    assert h[-1]["content"] == "hola real" and h[-1]["tokens"] == 30
