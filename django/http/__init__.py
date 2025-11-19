"""Simplified HTTP primitives compatible with the tests."""  # noqa: D205
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HttpRequest:
    method: str = "GET"
    path: str = "/"
    body: bytes | None = None
    user: Any | None = None


class HttpResponse:
    """Very small subset of Django's :class:`HttpResponse`."""

    def __init__(self, content: Any = b"", status: int = 200) -> None:
        if isinstance(content, str):
            content = content.encode("utf-8")
        self.content: bytes = content or b""
        self.status_code = status

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"HttpResponse(status_code={self.status_code}, content={self.content!r})"


__all__ = ["HttpRequest", "HttpResponse"]
