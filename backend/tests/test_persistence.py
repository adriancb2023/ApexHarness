from fastapi.testclient import TestClient

from app.main import create_app


def test_proyectos_y_sesiones_sobreviven_a_reinicio(tmp_path):
    db = str(tmp_path / "harness.db")

    c1 = TestClient(create_app(gateway_fake=True, db_path=db))
    p = c1.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c1.post("/api/sessions", json={"project_id": p["id"], "title": "s1"}).json()

    c2 = TestClient(create_app(gateway_fake=True, db_path=db))
    ids = [x["id"] for x in c2.get(f"/api/sessions?project_id={p['id']}").json()]
    assert ids == [s["id"]]


def test_mensajes_y_tokens_sobreviven_a_reinicio(tmp_path):
    db = str(tmp_path / "harness.db")

    c1 = TestClient(create_app(gateway_fake=True, db_path=db))
    p = c1.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c1.post("/api/sessions", json={"project_id": p["id"], "title": "s1"}).json()
    c1.post(f"/api/sessions/{s['id']}/messages", json={"content": "hola", "feature": "users"})

    c2 = TestClient(create_app(gateway_fake=True, db_path=db))
    h = c2.get(f"/api/sessions/{s['id']}/messages").json()
    assert [m["role"] for m in h] == ["user", "assistant"]
    summ = c2.get(f"/api/tokens/summary?project_id={p['id']}").json()
    assert summ["total_tokens"] > 0
    assert summ["by_feature"]["users"] == summ["total_tokens"]
