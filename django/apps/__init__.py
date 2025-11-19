"""Simplified :mod:`django.apps` helpers."""


class AppConfig:
    """Tiny subset of Django's :class:`AppConfig`."""

    default_auto_field = "django.db.models.AutoField"

    def __init__(self, name: str, app_module=None) -> None:
        self.name = name
        self.label = name.split(".")[-1]
        self.module = app_module

    def ready(self) -> None:  # pragma: no cover - hook for parity only
        """Hook provided for API compatibility."""


__all__ = ["AppConfig"]
