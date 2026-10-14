from fastapi.testclient import TestClient

from app.main import create_app


def test_lee_archivo_dentro_del_cwd(tmp_path):
    c = TestClient(create_app(gateway_fake=True))
    root = tmp_path / "proj"
    root.mkdir()
    (root / "a.py").write_text("print(1)", encoding="utf-8")
    p = c.post("/api/projects", json={"name": "A", "cwd": str(root)}).json()

    r = c.get(f"/api/files?project_id={p['id']}&path=a.py").json()
    assert r == {"path": "a.py", "content": "print(1)"}


def test_bloquea_escape_del_cwd(tmp_path):
    c = TestClient(create_app(gateway_fake=True))
    root = tmp_path / "proj"
    root.mkdir()
    (tmp_path / "secreto.txt").write_text("x", encoding="utf-8")
    p = c.post("/api/projects", json={"name": "A", "cwd": str(root)}).json()

    assert c.get(f"/api/files?project_id={p['id']}&path=../secreto.txt").status_code == 403
    assert c.get("/api/files?project_id=nope&path=a.py").status_code == 404
