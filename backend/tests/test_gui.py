from fastapi.testclient import TestClient

from app.main import create_app


def test_gui_sirve_selector_proyectos():
    c = TestClient(create_app(gateway_fake=True))
    r = c.get("/")
    assert r.status_code == 200
    assert 'id="project-selector"' in r.text
    assert 'id="session-list"' in r.text


def test_gui_tiene_chat_y_estado():
    c = TestClient(create_app(gateway_fake=True))
    r = c.get("/")
    assert 'id="chat-log"' in r.text
    assert 'id="chat-input"' in r.text
    assert 'id="task-status"' in r.text
