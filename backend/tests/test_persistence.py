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


def test_kanban_debate_locks_sobreviven_a_reinicio(tmp_path):
    db = str(tmp_path / "harness.db")

    c1 = TestClient(create_app(gateway_fake=True, db_path=db))
    p = c1.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    a = c1.post("/api/cards", json={"project_id": p["id"], "title": "API"}).json()
    b = c1.post("/api/cards", json={"project_id": p["id"], "title": "UI", "depends_on": [a["id"]]}).json()
    c1.patch(f"/api/cards/{a['id']}", json={"status": "listo"})

    be = c1.post("/api/sessions", json={"project_id": p["id"], "title": "be"}).json()
    fe = c1.post("/api/sessions", json={"project_id": p["id"], "title": "fe"}).json()
    d = c1.post(
        "/api/debates",
        json={"project_id": p["id"], "backend_session_id": be["id"], "frontend_session_id": fe["id"]},
    ).json()
    c1.post(f"/api/debates/{d['id']}/propose", json={"from": "backend", "content": "v1"})
    c1.post(f"/api/debates/{d['id']}/approve", json={"approve": True})
    c1.post("/api/locks", json={"path": "src/api.py", "locked_by": "backend"})

    c2 = TestClient(create_app(gateway_fake=True, db_path=db))
    cards = {x["id"]: x for x in c2.get(f"/api/cards?project_id={p['id']}").json()}
    assert cards[b["id"]]["blocked"] is False
    det = c2.get(f"/api/debates/{d['id']}").json()
    assert det["turn_count"] == 1
    assert det["turns"][0]["content"] == "v1"
    assert c2.get("/api/locks").json()[0]["locked_by"] == "backend"
