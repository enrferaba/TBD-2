"""Lightweight stand-in for :mod:`django.conf`."""
from __future__ import annotations

import importlib
import os
from types import ModuleType
from typing import Any


class LazySettings:
    """Lazy loader that mirrors the real Django ``settings`` object."""

    def __init__(self) -> None:
        self._wrapped: ModuleType | None = None

    @property
    def configured(self) -> bool:
        return self._wrapped is not None

    def _setup(self) -> ModuleType:
        if self._wrapped is not None:
            return self._wrapped
        module_path = os.environ.get("DJANGO_SETTINGS_MODULE")
        if not module_path:
            raise RuntimeError("DJANGO_SETTINGS_MODULE is not defined")
        module = importlib.import_module(module_path)
        self._wrapped = module
        return module

    def __getattr__(self, attr: str) -> Any:
        module = self._wrapped or self._setup()
        return getattr(module, attr)


settings = LazySettings()

__all__ = ["settings", "LazySettings"]
