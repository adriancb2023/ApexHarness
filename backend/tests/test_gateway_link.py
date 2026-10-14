import httpx

from app.gateway import ServeGateway, load_config
from app.main import create_app
from fastapi.testclient import TestClient


def _mock_serve():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [
            {"id": "ses_9", "title": "Real",
             "tokens": {"input": 100, "output": 20, "reasoning": 5, "cache": {"read": 0, "write": 0}},
             "cost": 0.0, "location": {"directory": "C:/p"}}
        ]})
    return ServeGateway(base_url="http://x:1", password="pw",
                        client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_sesion_vinculada_usa_tokens_reales():
    c = TestClient(create_app(gateway_fake=True, gateway=_mock_serve()))
    p = c.post("/api/projects", json={"name": "A", "cwd": "C:/tmp/A"}).json()
    s = c.post("/api/sessions", json={"project_id": p["id"], "opencode_session_id": "ses_9"}).json()
    assert s["opencode_session_id"] == "ses_9"

    listed = c.get("/api/opencode/sessions").json()
    assert listed[0]["id"] == "ses_9"

    summ = c.get(f"/api/tokens/summary?project_id={p['id']}").json()
    assert summ["by_session"][s["id"]] == 125


def test_config_defaults_y_env(monkeypatch):
    for k in ("HARNESS_DB", "HARNESS_QDRANT", "HARNESS_OPENCODE", "HARNESS_GATEWAY"):
        monkeypatch.delenv(k, raising=False)
    cfg = load_config()
    assert cfg["db_path"] is None and cfg["gateway"] == "fake"

    monkeypatch.setenv("HARNESS_DB", "x.db")
    monkeypatch.setenv("HARNESS_GATEWAY", "serve")
    cfg2 = load_config()
    assert cfg2["db_path"] == "x.db" and cfg2["gateway"] == "serve"
