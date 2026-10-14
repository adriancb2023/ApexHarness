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
