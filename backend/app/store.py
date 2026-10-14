"""Repositorios de persistencia operativa.

Memoria para tests, SQLite file para producción. Misma interfaz.
"""

import json
import sqlite3


class MemoryStore:
    def __init__(self):
        self._projects: dict[str, dict] = {}
        self._sessions: dict[str, dict] = {}
        self._messages: dict[str, list] = {}
        self._feature_tokens: dict[str, dict[str, int]] = {}
        self._cards: dict[str, dict] = {}
        self._debates: dict[str, dict] = {}
        self._locks: dict[str, dict] = {}

    def save_project(self, project: dict) -> None:
        self._projects[project["id"]] = dict(project)

    def get_project(self, pid: str) -> dict | None:
        p = self._projects.get(pid)
        return dict(p) if p else None

    def save_session(self, session: dict) -> None:
        self._sessions[session["id"]] = dict(session)

    def get_session(self, sid: str) -> dict | None:
        s = self._sessions.get(sid)
        return dict(s) if s else None

    def list_sessions(self, project_id: str) -> list[dict]:
        return [dict(s) for s in self._sessions.values() if s["project_id"] == project_id]

    def add_session_tokens(self, sid: str, amount: int) -> None:
        if sid in self._sessions:
            self._sessions[sid]["tokens"] = self._sessions[sid].get("tokens", 0) + amount

    def append_message(self, sid: str, message: dict) -> None:
        self._messages.setdefault(sid, []).append(dict(message))

    def list_messages(self, sid: str) -> list[dict]:
        return [dict(m) for m in self._messages.get(sid, [])]

    def add_feature_tokens(self, project_id: str, feature: str, amount: int) -> None:
        self._feature_tokens.setdefault(project_id, {}).setdefault(feature, 0)
        self._feature_tokens[project_id][feature] += amount

    def get_feature_tokens(self, project_id: str) -> dict[str, int]:
        return dict(self._feature_tokens.get(project_id, {}))

    # --- Kanban / debates / locks (ticket 2A-03) ---

    def save_card(self, card: dict) -> None:
        self._cards[card["id"]] = dict(card)

    def get_card(self, cid: str) -> dict | None:
        c = self._cards.get(cid)
        return dict(c) if c else None

    def list_cards(self, project_id: str) -> list[dict]:
        return [dict(c) for c in self._cards.values() if c["project_id"] == project_id]

    def set_card_status(self, cid: str, status: str) -> None:
        if cid in self._cards:
            self._cards[cid]["status"] = status

    def save_debate(self, debate: dict) -> None:
        self._debates[debate["id"]] = json.loads(json.dumps(debate))

    def get_debate(self, did: str) -> dict | None:
        d = self._debates.get(did)
        return json.loads(json.dumps(d)) if d else None

    def get_lock(self, path: str) -> dict | None:
        l = self._locks.get(path)
        return dict(l) if l else None

    def save_lock(self, lock: dict) -> None:
        self._locks[lock["path"]] = dict(lock)

    def delete_lock(self, path: str) -> None:
        self._locks.pop(path, None)

    def list_locks(self) -> list[dict]:
        return [dict(l) for l in self._locks.values()]


class SqliteStore:
    def __init__(self, path: str):
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, name TEXT, cwd TEXT)"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS sessions"
            " (id TEXT PRIMARY KEY, project_id TEXT, title TEXT, cwd TEXT, tokens INTEGER DEFAULT 0)"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS messages"
            " (sid TEXT, seq INTEGER PRIMARY KEY AUTOINCREMENT,"
            " role TEXT, content TEXT, tokens INTEGER, ts REAL, feature TEXT)"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS feature_tokens"
            " (project_id TEXT, feature TEXT, tokens INTEGER DEFAULT 0,"
            " PRIMARY KEY (project_id, feature))"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS cards"
            " (id TEXT PRIMARY KEY, project_id TEXT, title TEXT, feature TEXT,"
            " files TEXT, depends_on TEXT, status TEXT)"
        )
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS debates"
            " (id TEXT PRIMARY KEY, project_id TEXT, backend_session_id TEXT,"
            " frontend_session_id TEXT, turns TEXT, pending TEXT,"
            " turn_count INTEGER DEFAULT 0, status TEXT)"
        )
        self._db.execute("CREATE TABLE IF NOT EXISTS locks (path TEXT PRIMARY KEY, locked_by TEXT)")
        self._db.commit()

    def save_project(self, project: dict) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO projects (id, name, cwd) VALUES (?, ?, ?)",
            (project["id"], project["name"], project["cwd"]),
        )
        self._db.commit()

    def get_project(self, pid: str) -> dict | None:
        row = self._db.execute("SELECT id, name, cwd FROM projects WHERE id = ?", (pid,)).fetchone()
        return {"id": row[0], "name": row[1], "cwd": row[2]} if row else None

    def save_session(self, session: dict) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO sessions (id, project_id, title, cwd, tokens)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                session["id"],
                session["project_id"],
                session["title"],
                session["cwd"],
                session.get("tokens", 0),
            ),
        )
        self._db.commit()

    def get_session(self, sid: str) -> dict | None:
        row = self._db.execute(
            "SELECT id, project_id, title, cwd, tokens FROM sessions WHERE id = ?", (sid,)
        ).fetchone()
        if not row:
            return None
        return {"id": row[0], "project_id": row[1], "title": row[2], "cwd": row[3], "tokens": row[4]}

    def list_sessions(self, project_id: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, project_id, title, cwd, tokens FROM sessions WHERE project_id = ?",
            (project_id,),
        ).fetchall()
        return [
            {"id": r[0], "project_id": r[1], "title": r[2], "cwd": r[3], "tokens": r[4]} for r in rows
        ]

    def add_session_tokens(self, sid: str, amount: int) -> None:
        self._db.execute("UPDATE sessions SET tokens = tokens + ? WHERE id = ?", (amount, sid))
        self._db.commit()

    def append_message(self, sid: str, message: dict) -> None:
        self._db.execute(
            "INSERT INTO messages (sid, role, content, tokens, ts, feature)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                sid,
                message["role"],
                message["content"],
                message.get("tokens", 0),
                message.get("ts", 0.0),
                message.get("feature", ""),
            ),
        )
        self._db.commit()

    def list_messages(self, sid: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT role, content, tokens, ts, feature FROM messages WHERE sid = ? ORDER BY seq",
            (sid,),
        ).fetchall()
        return [
            {"role": r[0], "content": r[1], "tokens": r[2], "ts": r[3], "feature": r[4]} for r in rows
        ]

    def add_feature_tokens(self, project_id: str, feature: str, amount: int) -> None:
        self._db.execute(
            "INSERT INTO feature_tokens (project_id, feature, tokens) VALUES (?, ?, ?)"
            " ON CONFLICT (project_id, feature) DO UPDATE SET tokens = tokens + ?",
            (project_id, feature, amount, amount),
        )
        self._db.commit()

    def get_feature_tokens(self, project_id: str) -> dict[str, int]:
        rows = self._db.execute(
            "SELECT feature, tokens FROM feature_tokens WHERE project_id = ?", (project_id,)
        ).fetchall()
        return {r[0]: r[1] for r in rows}

    def save_card(self, card: dict) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO cards (id, project_id, title, feature, files, depends_on, status)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                card["id"],
                card["project_id"],
                card["title"],
                card.get("feature", ""),
                json.dumps(card.get("files", [])),
                json.dumps(card.get("depends_on", [])),
                card.get("status", "backlog"),
            ),
        )
        self._db.commit()

    def _row_to_card(self, r) -> dict:
        return {
            "id": r[0],
            "project_id": r[1],
            "title": r[2],
            "feature": r[3],
            "files": json.loads(r[4]),
            "depends_on": json.loads(r[5]),
            "status": r[6],
        }

    def get_card(self, cid: str) -> dict | None:
        row = self._db.execute(
            "SELECT id, project_id, title, feature, files, depends_on, status"
            " FROM cards WHERE id = ?",
            (cid,),
        ).fetchone()
        return self._row_to_card(row) if row else None

    def list_cards(self, project_id: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, project_id, title, feature, files, depends_on, status"
            " FROM cards WHERE project_id = ?",
            (project_id,),
        ).fetchall()
        return [self._row_to_card(r) for r in rows]

    def set_card_status(self, cid: str, status: str) -> None:
        self._db.execute("UPDATE cards SET status = ? WHERE id = ?", (status, cid))
        self._db.commit()

    def save_debate(self, debate: dict) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO debates (id, project_id, backend_session_id,"
            " frontend_session_id, turns, pending, turn_count, status)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                debate["id"],
                debate["project_id"],
                debate["backend_session_id"],
                debate["frontend_session_id"],
                json.dumps(debate.get("turns", [])),
                json.dumps(debate.get("pending")),
                debate.get("turn_count", 0),
                debate.get("status", "open"),
            ),
        )
        self._db.commit()

    def get_debate(self, did: str) -> dict | None:
        row = self._db.execute(
            "SELECT id, project_id, backend_session_id, frontend_session_id,"
            " turns, pending, turn_count, status FROM debates WHERE id = ?",
            (did,),
        ).fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "project_id": row[1],
            "backend_session_id": row[2],
            "frontend_session_id": row[3],
            "turns": json.loads(row[4]),
            "pending": json.loads(row[5]),
            "turn_count": row[6],
            "status": row[7],
        }

    def get_lock(self, path: str) -> dict | None:
        row = self._db.execute("SELECT path, locked_by FROM locks WHERE path = ?", (path,)).fetchone()
        return {"path": row[0], "locked_by": row[1]} if row else None

    def save_lock(self, lock: dict) -> None:
        self._db.execute(
            "INSERT OR REPLACE INTO locks (path, locked_by) VALUES (?, ?)",
            (lock["path"], lock["locked_by"]),
        )
        self._db.commit()

    def delete_lock(self, path: str) -> None:
        self._db.execute("DELETE FROM locks WHERE path = ?", (path,))
        self._db.commit()

    def list_locks(self) -> list[dict]:
        return [
            {"path": r[0], "locked_by": r[1]}
            for r in self._db.execute("SELECT path, locked_by FROM locks").fetchall()
        ]
