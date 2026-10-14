"""Puerta de enlace hacia OpenCode.

Fake para tests y desarrollo sin serve; Serve real contra `serve` v2.
"""

import base64
import json
import os
import re
import subprocess

import httpx


def estimate_tokens(content: str) -> int:
    return max(1, len(content) // 4 + 1)


class OpencodeGateway:
    def send(self, content: str) -> dict:
        raise NotImplementedError

    def deltas(self, content: str) -> list[str]:
        raise NotImplementedError

    def list_sessions(self) -> list:
        raise NotImplementedError

    def linked_tokens(self, opencode_session_id: str) -> int | None:
        raise NotImplementedError


class FakeGateway(OpencodeGateway):
    def send(self, content: str) -> dict:
        reply = f"eco: {content}"
        tok_u = estimate_tokens(content)
        tok_a = estimate_tokens(reply)
        return {"reply": reply, "tokens_user": tok_u, "tokens_reply": tok_a, "tokens": tok_u + tok_a}

    def deltas(self, content: str) -> list[str]:
        return ["eco: ", content]

    def list_sessions(self) -> list:
        return []

    def linked_tokens(self, opencode_session_id: str) -> int | None:
        return None


def _normalize_session(raw: dict) -> dict:
    toks = raw.get("tokens", {})
    return {
        "id": raw.get("id", ""),
        "title": raw.get("title", ""),
        "tokens": toks.get("input", 0) + toks.get("output", 0) + toks.get("reasoning", 0),
        "cost": raw.get("cost", 0),
        "directory": (raw.get("location") or {}).get("directory", ""),
    }


class ServeGateway(OpencodeGateway):
    def __init__(self, base_url: str, password: str, client=None):
        self.base_url = base_url.rstrip("/")
        self._auth = "Basic " + base64.b64encode(f"opencode:{password}".encode()).decode()
        self._client = client or httpx.Client(timeout=30.0)

    def _get(self, path: str) -> dict:
        r = self._client.get(self.base_url + path, headers={"Authorization": self._auth})
        r.raise_for_status()
        return r.json()

    def list_sessions(self) -> list:
        return [_normalize_session(s) for s in self._get("/api/session").get("data", [])]

    def get_tokens(self, session_id: str) -> int:
        for s in self.list_sessions():
            if s["id"] == session_id:
                return s["tokens"]
        return 0

    def linked_tokens(self, opencode_session_id: str) -> int | None:
        return self.get_tokens(opencode_session_id)

    def send(self, content: str) -> dict:
        raise NotImplementedError("ticket 03")

    def deltas(self, content: str) -> list[str]:
        raise NotImplementedError("ticket 03")


def service_password(path: str | None = None) -> str | None:
    candidate = path or os.path.join(os.path.expanduser("~"), ".config", "opencode", "service.json")
    try:
        with open(candidate, encoding="utf-8") as f:
            return json.load(f).get("password")
    except OSError:
        return None


def _opencode_bin() -> str | None:
    import shutil

    found = shutil.which("opencode")
    if found and not found.endswith(".ps1"):
        return found
    candidate = os.path.join(
        os.environ.get("APPDATA", ""), "npm", "node_modules", "@opencode", "cli", "bin", "opencode.exe"
    )
    return candidate if os.path.exists(candidate) else found


def discover_base_url() -> str | None:
    if os.environ.get("HARNESS_OPENCODE"):
        return os.environ["HARNESS_OPENCODE"]
    exe = _opencode_bin()
    if not exe:
        return None
    try:
        out = subprocess.run(
            [exe, "service", "status"], capture_output=True, text=True, timeout=10
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    match = re.search(r"https?://[^\s]+", out)
    return match.group(0) if match else None


def load_config() -> dict:
    return {
        "db_path": os.environ.get("HARNESS_DB"),
        "qdrant_path": os.environ.get("HARNESS_QDRANT"),
        "opencode_url": os.environ.get("HARNESS_OPENCODE") or discover_base_url(),
        "opencode_password": os.environ.get("HARNESS_OPENCODE_PASSWORD") or service_password(),
        "gateway": os.environ.get("HARNESS_GATEWAY", "fake"),
    }
