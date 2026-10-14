from fastapi.testclient import TestClient

from app.main import create_app


def test_ws_streams_deltas_y_done():
    c = TestClient(create_app(gateway_fake=True))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c.post("/api/sessions", json={"project_id": p["id"], "title": "s1"}).json()

    with c.websocket_connect(f"/ws/sessions/{s['id']}") as ws:
        ws.send_json({"content": "hola mundo"})
        deltas = []
        done = None
        for _ in range(10):
            msg = ws.receive_json()
            if "delta" in msg:
                deltas.append(msg["delta"])
            if msg.get("done"):
                done = msg
                break
        assert done is not None
        assert done["status"] == "done"
        assert "hola" in "".join(deltas)

    h = c.get(f"/api/sessions/{s['id']}/messages").json()
    assert [m["role"] for m in h[-2:]] == ["user", "assistant"]
