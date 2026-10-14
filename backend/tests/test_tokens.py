from fastapi.testclient import TestClient

from app.main import create_app


def test_tokens_por_sesion_proyecto_y_feature():
    c = TestClient(create_app(gateway_fake=True))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c.post("/api/sessions", json={"project_id": p["id"], "title": "s1"}).json()

    c.post(f"/api/sessions/{s['id']}/messages", json={"content": "hola"}).json()
    c.post(
        f"/api/sessions/{s['id']}/messages",
        json={"content": "tabla users", "feature": "users"},
    ).json()

    summ = c.get(f"/api/tokens/summary?project_id={p['id']}").json()
    assert summ["project_id"] == p["id"]
    assert summ["total_tokens"] > 0
    assert summ["by_session"][s["id"]] == summ["total_tokens"]
    assert summ["by_feature"]["users"] > 0

    h = c.get(f"/api/sessions/{s['id']}/messages").json()
    assert all("ts" in m and "tokens" in m for m in h)
