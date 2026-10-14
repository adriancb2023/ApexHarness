from fastapi.testclient import TestClient

from app.main import create_app


def _duo(c: TestClient):
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    b = c.post("/api/sessions", json={"project_id": p["id"], "title": "be"}).json()
    f = c.post("/api/sessions", json={"project_id": p["id"], "title": "fe"}).json()
    d = c.post(
        "/api/debates",
        json={"project_id": p["id"], "backend_session_id": b["id"], "frontend_session_id": f["id"]},
    ).json()
    return p, b, f, d


def test_stepping_entrega_solo_al_aprobar():
    c = TestClient(create_app(gateway_fake=True))
    _, b, f, d = _duo(c)

    r = c.post(f"/api/debates/{d['id']}/propose", json={"from": "backend", "content": "contrato v1"}).json()
    assert r["status"] == "waiting_approval"

    det = c.get(f"/api/debates/{d['id']}").json()
    assert det["turn_count"] == 0
    assert det["pending"]["content"] == "contrato v1"

    ok = c.post(f"/api/debates/{d['id']}/approve", json={"approve": True}).json()
    assert ok["status"] == "open"
    assert ok["turn_count"] == 1

    det2 = c.get(f"/api/debates/{d['id']}").json()
    assert det2["turns"][0]["to"] == "frontend"


def test_cap_5_turnos_pide_intervencion():
    c = TestClient(create_app(gateway_fake=True))
    _, b, f, d = _duo(c)

    remitente = "backend"
    for _ in range(5):
        c.post(f"/api/debates/{d['id']}/propose", json={"from": remitente, "content": "ping"}).json()
        c.post(f"/api/debates/{d['id']}/approve", json={"approve": True}).json()
        remitente = "frontend" if remitente == "backend" else "backend"

    r = c.post(f"/api/debates/{d['id']}/propose", json={"from": remitente, "content": "extra"})
    assert r.status_code == 409
    assert c.get(f"/api/debates/{d['id']}").json()["status"] == "needs_intervention"
