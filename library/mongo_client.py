"""Helpers para conectarse a MongoDB usando PyMongo."""
from __future__ import annotations

from django.conf import settings
from pymongo import MongoClient

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    """Crear (o reutilizar) un cliente Mongo compartido."""

    global _client
    if _client is None:
        uri = getattr(settings, "MONGO_URI", "mongodb://mongo:27017/biblioteca_online")
        _client = MongoClient(uri)
    return _client


def get_mongo_database():
    """Obtener la base de datos principal configurada en settings."""

    client = get_mongo_client()
    db_name = getattr(settings, "MONGO_DB_NAME", None)
    if db_name:
        return client[db_name]
    return client.get_default_database()


def get_activity_collection():
    """Devolver la colección donde se registran los eventos de actividad."""

    collection_name = getattr(settings, "MONGO_ACTIVITY_COLLECTION", "activity_logs")
    return get_mongo_database()[collection_name]
