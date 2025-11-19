"""Bare-bones routing helpers."""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

View = Callable[..., Any]


def _split(path: str) -> list[str]:
    normalized = path.strip("/")
    if not normalized:
        return []
    return normalized.split("/")


@dataclass
class Route:
    pattern: str
    callback: View
    name: str | None = None
    kwargs: dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def matches(self, request_path: str) -> bool:
        pattern_parts = _split(self.pattern)
        request_parts = _split(request_path)
        if len(pattern_parts) != len(request_parts):
            return False
        resolved_kwargs: dict[str, Any] = {}
        for pattern_part, request_part in zip(pattern_parts, request_parts):
            if pattern_part.startswith("<") and pattern_part.endswith(">"):
                converter, _, param_name = pattern_part[1:-1].partition(":")
                if not param_name:
                    param_name = converter
                    converter = "str"
                if converter in {"int", "slug"}:
                    if not request_part.isdigit():
                        return False
                    resolved_kwargs[param_name] = int(request_part)
                else:
                    resolved_kwargs[param_name] = request_part
                continue
            if pattern_part != request_part:
                return False
        self.kwargs = resolved_kwargs
        return True


def path(route: str, view: View, name: str | None = None) -> Route:
    return Route(route, view, name)


def include(arg: str | Sequence[Route]) -> Iterable[Route]:
    if isinstance(arg, str):
        module = importlib.import_module(arg)
        return getattr(module, "urlpatterns", [])
    return arg


def resolve(request_path: str) -> Route:
    from django.conf import settings

    module = importlib.import_module(settings.ROOT_URLCONF)
    for entry in getattr(module, "urlpatterns", []):
        if isinstance(entry, Route) and entry.matches(request_path):
            return entry
    raise LookupError(f"No route matches {request_path}")


__all__ = ["include", "path", "resolve", "Route"]
