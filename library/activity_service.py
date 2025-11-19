"""Servicio mínimo para registrar y consultar actividad en MongoDB."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, List

from .mongo_client import get_activity_collection


def log_activity(event_type: str, payload: Dict[str, Any] | None = None) -> str:
    """Guardar un evento de actividad y devolver su identificador."""

    document = {
        "event_type": event_type,
        "payload": payload or {},
        "created_at": datetime.now(tz=UTC).isoformat(),
    }
    result = get_activity_collection().insert_one(document)
    return str(result.inserted_id)


def list_recent_activity(limit: int = 20) -> List[Dict[str, Any]]:
    """Obtener los eventos más recientes ordenados por `created_at`."""

    documents = list(get_activity_collection().find())
    documents.sort(key=lambda doc: doc.get("created_at", ""), reverse=True)
    return documents[:limit]
