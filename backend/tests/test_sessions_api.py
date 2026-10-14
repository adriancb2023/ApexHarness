from fastapi.testclient import TestClient

from app.main import create_app


def test_sesiones_aisladas_por_proyecto():
    app = create_app(gateway_fake=True)
    c = TestClient(app)

    assert c.get("/health").json() == {"ok": True}

    pa = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    pb = c.post("/api/projects", json={"name": "B", "cwd": "C:/tmp/B"}).json()

    sa = c.post("/api/sessions", json={"project_id": pa["id"], "title": "s-a1"}).json()
    assert sa["project_id"] == pa["id"]
    assert sa["cwd"] == "C:/tmp/A"

    la = c.get(f"/api/sessions?project_id={pa['id']}").json()
    lb = c.get(f"/api/sessions?project_id={pb['id']}").json()
    assert [s["id"] for s in la] == [sa["id"]]
    assert lb == []
