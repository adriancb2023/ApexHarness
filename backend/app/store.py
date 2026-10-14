"""Repositorios de persistencia operativa.

Memoria para tests, SQLite file para producción. Misma interfaz.
"""

import sqlite3


class MemoryStore:
    def __init__(self):
        self._projects: dict[str, dict] = {}
        self._sessions: dict[str, dict] = {}
        self._messages: dict[str, list] = {}
        self._feature_tokens: dict[str, dict[str, int]] = {}

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
