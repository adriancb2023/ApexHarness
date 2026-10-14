import hashlib
import time
import uuid
from pathlib import Path

from typing import Literal

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
    feature: str = ""


class CardIn(BaseModel):
    project_id: str
    title: str
    feature: str = ""
    files: list[str] = []
    depends_on: list[str] = []


class CardPatch(BaseModel):
    status: Literal["backlog", "progreso", "pruebas", "listo"]


class EngramIn(BaseModel):
    card_id: str
    problema: str
    solucion: str = ""
    archivos: list[str] = []
    lecciones: str = ""


def _embed(text: str, dim: int = 64) -> list[float]:
    import re

    vec = [0.0] * dim
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        idx = int(hashlib.md5(w.encode()).hexdigest(), 16) % dim
        vec[idx] += 1.0
    norm = sum(v * v for v in vec) ** 0.5
    return [v / norm for v in vec] if norm else vec


def _fake_tokens(content: str) -> int:
    return max(1, len(content) // 4 + 1)


def create_app(gateway_fake: bool = True) -> FastAPI:
    app = FastAPI()
    projects: dict[str, dict] = {}
    sessions: dict[str, dict] = {}
    messages: dict[str, list] = {}
    cards: dict[str, dict] = {}
    feature_tokens: dict[str, dict[str, int]] = {}

    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, PointStruct, VectorParams

    qc = QdrantClient(":memory:")
    qc.recreate_collection("engrams", vectors_config=VectorParams(size=64, distance=Distance.COSINE))
    engram_seq: dict[str, int] = {}
    engram_counter = [0]

    def _card_view(card: dict) -> dict:
        done = {c["id"] for c in cards.values() if c["status"] == "listo"}
        return {**card, "blocked": any(d not in done for d in card["depends_on"])}

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
        tok_u = _fake_tokens(body.content)
        tok_a = _fake_tokens(reply)
        toks = tok_u + tok_a
        now = time.time()
        messages.setdefault(sid, []).append(
            {"role": "user", "content": body.content, "tokens": tok_u, "ts": now, "feature": body.feature}
        )
        messages[sid].append(
            {"role": "assistant", "content": reply, "tokens": tok_a, "ts": now, "feature": body.feature}
        )
        sessions[sid]["tokens"] = sessions[sid].get("tokens", 0) + toks
        if body.feature:
            pid = sessions[sid]["project_id"]
            feature_tokens.setdefault(pid, {}).setdefault(body.feature, 0)
            feature_tokens[pid][body.feature] += toks
        return {"reply": reply, "tokens": toks, "status": "done"}

    @app.get("/api/sessions/{sid}/messages")
    def get_messages(sid: str):
        if sid not in sessions:
            raise HTTPException(404, "session not found")
        return messages.get(sid, [])

    @app.get("/api/tokens/summary")
    def tokens_summary(project_id: str = ""):
        by_session = {
            s["id"]: s.get("tokens", 0)
            for s in sessions.values()
            if s["project_id"] == project_id
        }
        return {
            "project_id": project_id,
            "total_tokens": sum(by_session.values()),
            "by_session": by_session,
            "by_feature": feature_tokens.get(project_id, {}),
        }

    @app.post("/api/cards")
    def create_card(body: CardIn):
        cid = str(uuid.uuid4())[:8]
        cards[cid] = {
            "id": cid,
            "project_id": body.project_id,
            "title": body.title,
            "feature": body.feature,
            "files": body.files,
            "depends_on": body.depends_on,
            "status": "backlog",
        }
        return _card_view(cards[cid])

    @app.get("/api/cards")
    def list_cards(project_id: str = ""):
        return [_card_view(c) for c in cards.values() if c["project_id"] == project_id]

    @app.patch("/api/cards/{cid}")
    def patch_card(cid: str, body: CardPatch):
        if cid not in cards:
            raise HTTPException(404, "card not found")
        cards[cid]["status"] = body.status
        return _card_view(cards[cid])

    @app.post("/api/engrams")
    def consolidate_engram(body: EngramIn):
        card = cards.get(body.card_id)
        if card is None:
            raise HTTPException(404, "card not found")
        if card["status"] != "listo":
            raise HTTPException(409, "solo se consolida en Done")
        if body.card_id not in engram_seq:
            engram_counter[0] += 1
            engram_seq[body.card_id] = engram_counter[0]
        qc.upsert(
            collection_name="engrams",
            points=[
                PointStruct(
                    id=engram_seq[body.card_id],
                    vector=_embed(f"{body.problema} {body.solucion} {body.lecciones}"),
                    payload={
                        "card_id": body.card_id,
                        "problema": body.problema,
                        "solucion": body.solucion,
                        "archivos": body.archivos,
                        "lecciones": body.lecciones,
                    },
                )
            ],
        )
        return {"ok": True, "card_id": body.card_id}

    @app.get("/api/engrams/search")
    def search_engrams(q: str = "", limit: int = 5):
        res = qc.query_points(collection_name="engrams", query=_embed(q), limit=limit)
        return [
            {"card_id": h.payload["card_id"], "score": h.score, **h.payload}
            for h in res.points
        ]

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
            now = time.time()
            await ws.send_json({"delta": "eco: "})
            await ws.send_json({"delta": content})
            messages.setdefault(sid, []).append(
                {"role": "user", "content": content, "tokens": _fake_tokens(content), "ts": now, "feature": ""}
            )
            messages[sid].append(
                {"role": "assistant", "content": reply, "tokens": _fake_tokens(reply), "ts": now, "feature": ""}
            )
            sessions[sid]["tokens"] = sessions[sid].get("tokens", 0) + toks
            await ws.send_json({"done": True, "tokens": toks, "status": "done"})

    @app.get("/")
    def gui():
        return FileResponse(Path(__file__).parent.parent / "static" / "index.html")

    return app


app = create_app()
