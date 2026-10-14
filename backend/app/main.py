import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


class ProjectIn(BaseModel):
    name: str
    cwd: str


class SessionIn(BaseModel):
    project_id: str
    title: str = ""


def create_app(gateway_fake: bool = True) -> FastAPI:
    app = FastAPI()
    projects: dict[str, dict] = {}
    sessions: dict[str, dict] = {}

    @app.get("/health")
    def health():
        return {"ok": True}

    @app.post("/api/projects")
    def create_project(body: ProjectIn):
        pid = str(uuid.uuid4())[:8]
        projects[pid] = {"id": pid, "name": body.name, "cwd": body.cwd}
        return projects[pid]

    @app.post("/api/sessions")
    def create_session(body: SessionIn):
        proj = projects.get(body.project_id)
        if proj is None:
            raise HTTPException(404, "project not found")
        sid = str(uuid.uuid4())[:8]
        # gateway_fake: no llama a `opencode serve`, solo registra cwd aislado
        sessions[sid] = {
            "id": sid,
            "project_id": body.project_id,
            "title": body.title,
            "cwd": proj["cwd"],
        }
        return sessions[sid]

    @app.get("/api/sessions")
    def list_sessions(project_id: str = ""):
        return [s for s in sessions.values() if s["project_id"] == project_id]

    @app.get("/")
    def gui():
        return FileResponse(Path(__file__).parent.parent / "static" / "index.html")

    return app


app = create_app()
