from fastapi.testclient import TestClient

from app.main import create_app


def test_sirve_dist_si_existe_si_no_estatica(tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<html>DISTMARKER</html>", encoding="utf-8")

    c = TestClient(create_app(gateway_fake=True, frontend_dist=str(dist)))
    assert "DISTMARKER" in c.get("/").text

    c2 = TestClient(create_app(gateway_fake=True, frontend_dist=str(tmp_path / "nodist")))
    assert 'id="project-selector"' in c2.get("/").text
