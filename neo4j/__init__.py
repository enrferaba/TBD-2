"""Lightweight Neo4j driver stub for offline usage."""
from __future__ import annotations

from typing import Any, Dict


class _InMemorySession:
    def __init__(self, state: Dict[str, Any]) -> None:
        self._state = state

    def run(self, _: str, **__: Any) -> list[Any]:  # pragma: no cover - API placeholder
        return []

    def close(self) -> None:  # pragma: no cover - API placeholder
        return None


class _InMemoryDriver:
    def __init__(self, uri: str, auth: tuple[str, str] | None) -> None:
        self.uri = uri
        self.auth = auth or (None, None)
        self._graph_state: Dict[str, Any] = {"books": {}, "users": {}, "ratings": {}}

    def session(self) -> _InMemorySession:
        return _InMemorySession(self._graph_state)

    def close(self) -> None:  # pragma: no cover - API placeholder
        return None


class GraphDatabase:
    """Expose the same constructor the official driver offers."""

    @staticmethod
    def driver(uri: str, auth: tuple[str, str] | None = None) -> _InMemoryDriver:
        return _InMemoryDriver(uri, auth)


__all__ = ["GraphDatabase"]
