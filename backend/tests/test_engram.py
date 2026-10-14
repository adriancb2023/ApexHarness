from fastapi.testclient import TestClient

from app.main import create_app


def _lista(c: TestClient, pid: str, titulo: str):
    a = c.post("/api/cards", json={"project_id": pid, "title": titulo}).json()
    c.patch(f"/api/cards/{a['id']}", json={"status": "listo"})
    return a


def test_consolida_solo_en_done_y_recupera():
    c = TestClient(create_app(gateway_fake=True))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()

    pendiente = c.post("/api/cards", json={"project_id": p["id"], "title": "WIP"}).json()
    r = c.post(
        "/api/engrams",
        json={"card_id": pendiente["id"], "problema": "x", "solucion": "y"},
    )
    assert r.status_code == 409

    a = _lista(c, p["id"], "Auth con JWT expira")
    b = _lista(c, p["id"], "Export CSV de reportes")

    assert (
        c.post(
            "/api/engrams",
            json={
                "card_id": a["id"],
                "problema": "JWT expira y rompe sesión",
                "solucion": "refresh token rotativo",
                "archivos": ["auth.py"],
                "lecciones": "renovar antes de expirar",
            },
        ).status_code
        == 200
    )
    c.post(
        "/api/engrams",
        json={
            "card_id": b["id"],
            "problema": "CSV enorme agota memoria",
            "solucion": "streaming por chunks",
            "archivos": ["export.py"],
            "lecciones": "nunca cargar todo en RAM",
        },
    )

    res = c.get("/api/engrams/search", params={"q": "refresh token JWT sesión"}).json()
    assert res[0]["card_id"] == a["id"]
