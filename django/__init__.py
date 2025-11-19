"""Minimal Django-like stubs for offline development."""
from .conf import settings  # noqa: F401


def setup():
    """Populate the settings object based on ``DJANGO_SETTINGS_MODULE``."""
    settings._setup()


__all__ = ["setup", "settings"]
