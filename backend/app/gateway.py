"""Puerta de enlace hacia OpenCode.

Fake para tests y desarrollo sin serve; Serve real en el ticket 02.
"""


def estimate_tokens(content: str) -> int:
    return max(1, len(content) // 4 + 1)


class OpencodeGateway:
    def send(self, content: str) -> dict:
        raise NotImplementedError

    def deltas(self, content: str) -> list[str]:
        raise NotImplementedError


class FakeGateway(OpencodeGateway):
    def send(self, content: str) -> dict:
        reply = f"eco: {content}"
        tok_u = estimate_tokens(content)
        tok_a = estimate_tokens(reply)
        return {"reply": reply, "tokens_user": tok_u, "tokens_reply": tok_a, "tokens": tok_u + tok_a}

    def deltas(self, content: str) -> list[str]:
        return ["eco: ", content]
