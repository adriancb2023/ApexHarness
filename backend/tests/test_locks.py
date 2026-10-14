from fastapi.testclient import TestClient

from app.main import create_app


def test_lock_bloquea_avisa_y_libera():
    c = TestClient(create_app(gateway_fake=True))

    r = c.post("/api/locks", json={"path": "src/api.py", "locked_by": "backend"}).json()
    assert r["locked_by"] == "backend"

    conflicto = c.post("/api/locks", json={"path": "src/api.py", "locked_by": "frontend"})
    assert conflicto.status_code == 409
    assert conflicto.json()["locked_by"] == "backend"

    assert c.get("/api/locks").json()[0]["path"] == "src/api.py"

    assert c.delete("/api/locks", params={"path": "src/api.py", "locked_by": "frontend"}).status_code == 409
    assert c.delete("/api/locks", params={"path": "src/api.py", "locked_by": "backend"}).status_code == 200

    r2 = c.post("/api/locks", json={"path": "src/api.py", "locked_by": "frontend"}).json()
    assert r2["locked_by"] == "frontend"
