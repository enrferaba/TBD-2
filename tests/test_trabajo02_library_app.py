"""Tests asociados al Trabajo2."""
from __future__ import annotations

import os

import django
from django.conf import settings
from django.http import HttpRequest
from django.urls import resolve

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def test_trabajo02_app_registrada_en_installed_apps():
    assert "library" in settings.INSTALLED_APPS


def test_trabajo02_ruta_raiz_responde_200():
    route = resolve("/")
    response = route.callback(HttpRequest())
    assert response.status_code == 200
    assert response.content
