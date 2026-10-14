import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import FileResponse
from pydantic import BaseModel


class ProjectIn(BaseModel):
    name: str
    cwd: str


class SessionIn(BaseModel):
    project_id: str
    title: str = ""


class MessageIn(BaseModel):
    content: str


def _fake_tokens(content: str) -> int:
    return max(1, len(content) // 4 + 1)


def create_app(gateway_fake: bool = True) -> FastAPI:
    app = FastAPI()
    projects: dict[str, dict] = {}
    sessions: dict[str, dict] = {}
    messages: dict[str, list] = {}

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

    @app.post("/api/sessions/{sid}/messages")
    def post_message(sid: str, body: MessageIn):
        if sid not in sessions:
            raise HTTPException(404, "session not found")
        # gateway_fake: eco determinista en vez de `opencode serve`
        reply = f"eco: {body.content}"
        toks = _fake_tokens(body.content) + _fake_tokens(reply)
        messages.setdefault(sid, []).append({"role": "user", "content": body.content})
        messages[sid].append({"role": "assistant", "content": reply})
        sessions[sid]["tokens"] = sessions[sid].get("tokens", 0) + toks
        return {"reply": reply, "tokens": toks, "status": "done"}

    @app.get("/api/sessions/{sid}/messages")
    def get_messages(sid: str):
        if sid not in sessions:
            raise HTTPException(404, "session not found")
        return messages.get(sid, [])

    @app.websocket("/ws/sessions/{sid}")
    async def chat_ws(ws: WebSocket, sid: str):
        await ws.accept()
        if sid not in sessions:
            await ws.send_json({"error": "session not found"})
            await ws.close()
            return
        while True:
            try:
                data = await ws.receive_json()
            except Exception:
                break
            content = str(data.get("content", ""))
            reply = f"eco: {content}"
            toks = _fake_tokens(content) + _fake_tokens(reply)
            await ws.send_json({"delta": "eco: "})
            await ws.send_json({"delta": content})
            messages.setdefault(sid, []).append({"role": "user", "content": content})
            messages[sid].append({"role": "assistant", "content": reply})
            sessions[sid]["tokens"] = sessions[sid].get("tokens", 0) + toks
            await ws.send_json({"done": True, "tokens": toks, "status": "done"})

    @app.get("/")
    def gui():
        return FileResponse(Path(__file__).parent.parent / "static" / "index.html")

    return app


app = create_app()
