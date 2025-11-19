"""Biblioteca app package with Celery integration."""
from __future__ import annotations

from celery import Celery
from django.conf import settings


celery_app = Celery("library")
celery_app.conf["broker_url"] = getattr(settings, "CELERY_BROKER_URL", "redis://redis:6379/0")
celery_app.conf["result_backend"] = getattr(settings, "CELERY_RESULT_BACKEND", celery_app.conf["broker_url"])

__all__ = ["celery_app"]
