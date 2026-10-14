from fastapi.testclient import TestClient

from app.main import create_app


def _sesion(c: TestClient):
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    return c.post("/api/sessions", json={"project_id": p["id"], "title": "s1"}).json()


def test_post_message_guarda_historial_y_tokens():
    c = TestClient(create_app(gateway_fake=True))
    s = _sesion(c)

    r = c.post(f"/api/sessions/{s['id']}/messages", json={"content": "hola mundo"})
    assert r.status_code == 200
    body = r.json()
    assert body["tokens"] > 0
    assert body["status"] == "done"
    assert "hola" in body["reply"]

    h = c.get(f"/api/sessions/{s['id']}/messages").json()
    roles = [m["role"] for m in h]
    assert roles == ["user", "assistant"]
    assert h[0]["content"] == "hola mundo"


def test_historial_sesion_desconocida_404():
    c = TestClient(create_app(gateway_fake=True))
    assert c.get("/api/sessions/xxx/messages").status_code == 404
    assert c.post("/api/sessions/xxx/messages", json={"content": "x"}).status_code == 404
