"""Simplified APIView implementation."""
from __future__ import annotations

from typing import Any, Callable


class APIView:
    """Very small subset of DRF's APIView."""

    http_method_names = {"get", "post", "put", "patch", "delete"}

    @classmethod
    def as_view(cls, **initkwargs: Any) -> Callable[..., Any]:
        """Return a callable that instantiates the view per request."""

        def view(request: Any | None = None, *args: Any, **kwargs: Any) -> Any:
            self = cls(**initkwargs)
            method = getattr(request, "method", "GET").lower()
            if method not in cls.http_method_names:
                raise AttributeError(f"Method {method} not allowed")
            handler = getattr(self, method, None)
            if handler is None:
                raise AttributeError(f"Handler for {method} not implemented")
            return handler(request, *args, **kwargs)

        return view

    # Subclasses override e.g. `get`
    def get(self, request: Any | None = None, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - interface definition
        raise NotImplementedError
