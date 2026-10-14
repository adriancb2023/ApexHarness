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


def test_gui_tiene_kanban():
    c = TestClient(create_app(gateway_fake=True))
    r = c.get("/")
    assert 'id="kanban-board"' in r.text
    for col in ("backlog", "progreso", "pruebas", "listo"):
        assert f'data-col="{col}"' in r.text


def test_gui_tiene_panel_tokens():
    c = TestClient(create_app(gateway_fake=True))
    assert 'id="tokens-panel"' in c.get("/").text


def test_gui_tiene_vista_debate():
    c = TestClient(create_app(gateway_fake=True))
    html = c.get("/").text
    assert 'id="debate-view"' in html
    assert 'data-agent="backend"' in html
    assert 'data-agent="frontend"' in html
    assert 'id="approve-btn"' in html
