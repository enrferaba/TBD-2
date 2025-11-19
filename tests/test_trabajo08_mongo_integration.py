"""Tests asociados al Trabajo8 (integración básica con MongoDB)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.http import HttpRequest
from django.urls import resolve

from library.activity_service import log_activity
from library.mongo_client import get_activity_collection, get_mongo_client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def setup_function(_: object) -> None:
    get_activity_collection().delete_many({})


def _call(path: str):
    route = resolve(path)
    request = HttpRequest()
    request.method = "GET"
    request.path = path
    return route.callback(request, **route.kwargs)


def test_trabajo08_settings_tienen_mongo_uri():
    assert hasattr(settings, "MONGO_URI")
    assert settings.MONGO_URI.startswith("mongodb://")


def test_trabajo08_get_mongo_client_devuelve_cliente():
    client = get_mongo_client()
    assert client.server_info()["version"] == "fake-pymongo"


def test_trabajo08_get_activity_collection_devuelve_coleccion():
    collection = get_activity_collection()
    assert hasattr(collection, "insert_one")
    assert hasattr(collection, "find")


def test_trabajo08_log_activity_inserta_documento():
    log_activity("test", {"foo": "bar"})
    collection = get_activity_collection()
    assert collection.count_documents({"event_type": "test"}) == 1


def test_trabajo08_mongo_health_devuelve_200_y_status_ok():
    response = _call("/api/mongo/health/")
    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["mongo_status"] == "ok"
    assert "server_info" in payload
