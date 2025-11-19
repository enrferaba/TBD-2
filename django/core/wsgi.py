"""Stub for :mod:`django.core.wsgi`."""
from __future__ import annotations

from typing import Callable

Application = Callable[..., list[bytes]]


def get_wsgi_application() -> Application:
    """Return a callable placeholder."""

    def application(environ, start_response):  # pragma: no cover - unused helper
        raise NotImplementedError("WSGI server is not implemented in this stub")

    return application


__all__ = ["get_wsgi_application"]
