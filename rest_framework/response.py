"""Simplified Response object that returns JSON payloads."""
from __future__ import annotations

import json
from typing import Any


class Response:
    """Tiny stand-in for rest_framework.response.Response."""

    def __init__(self, data: Any, status: int = 200, *, content_type: str = "application/json") -> None:
        self.data = data
        self.status_code = status
        self.content_type = content_type
        self.content = self.render()

    def render(self) -> bytes:
        """Render the payload to JSON bytes."""
        return json.dumps(self.data).encode("utf-8")
