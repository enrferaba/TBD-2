"""Tests asociados al Trabajo3 (API básica)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.urls import resolve

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def test_trabajo03_api_health_ruta_resuelve_correctamente():
    route = resolve("/api/health/")
    assert route.name == "api-health"


def test_trabajo03_api_health_responde_200_y_json_ok():
    route = resolve("/api/health/")
    response = route.callback(None)
    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["status"] == "ok"
    assert payload["service"] == "Biblioteca Online"
