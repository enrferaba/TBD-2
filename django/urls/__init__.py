"""Bare-bones routing helpers."""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence

View = Callable[..., Any]


@dataclass
class Route:
    pattern: str
    callback: View
    name: str | None = None

    def matches(self, request_path: str) -> bool:
        normalized_pattern = self.pattern.strip("/")
        normalized_request = request_path.strip("/")
        return normalized_pattern == normalized_request


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
