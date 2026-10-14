from fastapi.testclient import TestClient

from app.main import create_app


def _proyecto(c: TestClient):
    return c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()


def test_tarjetas_dependencias_y_desbloqueo():
    c = TestClient(create_app(gateway_fake=True))
    p = _proyecto(c)

    a = c.post("/api/cards", json={"project_id": p["id"], "title": "API users"}).json()
    assert a["status"] == "backlog"
    assert a["blocked"] is False

    b = c.post(
        "/api/cards",
        json={"project_id": p["id"], "title": "Tabla users", "depends_on": [a["id"]]},
    ).json()
    assert b["blocked"] is True

    cards = c.get(f"/api/cards?project_id={p['id']}").json()
    bb = [x for x in cards if x["id"] == b["id"]][0]
    assert bb["blocked"] is True

    r = c.patch(f"/api/cards/{a['id']}", json={"status": "listo"})
    assert r.status_code == 200

    cards2 = c.get(f"/api/cards?project_id={p['id']}").json()
    bb2 = [x for x in cards2 if x["id"] == b["id"]][0]
    assert bb2["blocked"] is False


def test_transicion_invalida_422():
    c = TestClient(create_app(gateway_fake=True))
    p = _proyecto(c)
    a = c.post("/api/cards", json={"project_id": p["id"], "title": "X"}).json()
    r = c.patch(f"/api/cards/{a['id']}", json={"status": "volando"})
    assert r.status_code == 422
