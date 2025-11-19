"""Stub for :mod:`django.core.asgi`."""
from __future__ import annotations

from typing import Awaitable, Callable

Application = Callable[..., Awaitable[None]]


def get_asgi_application() -> Application:
    """Return a no-op ASGI callable for compatibility."""
    async def application(scope, receive, send):  # pragma: no cover - unused helper
        raise NotImplementedError("ASGI server is not implemented in this stub")

    return application


__all__ = ["get_asgi_application"]
