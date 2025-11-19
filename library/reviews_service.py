"""Servicio para gestionar reseñas de libros almacenadas en MongoDB."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Dict, List, Tuple

from django.conf import settings

from .mongo_client import get_mongo_database


def get_reviews_collection():
    """Obtener la colección de reseñas configurada para el proyecto."""

    collection_name = getattr(settings, "MONGO_REVIEWS_COLLECTION", "book_reviews")
    return get_mongo_database()[collection_name]


def create_review(
    *,
    book_id: int,
    user_id: int,
    username: str | None,
    rating: int | str,
    comment: str | None = None,
) -> Dict[str, Any]:
    """Insertar una reseña para un libro determinado y devolverla serializada."""

    normalized_rating = _normalize_rating(rating)
    normalized_comment = _normalize_comment(comment)
    timestamp = datetime.now(tz=UTC).isoformat()
    payload: Dict[str, Any] = {
        "book_id": book_id,
        "user_id": user_id,
        "username": username,
        "rating": normalized_rating,
        "comment": normalized_comment,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    result = get_reviews_collection().insert_one(payload)
    payload["_id"] = result.inserted_id
    return _serialize_review(payload)


def get_reviews_for_book(book_id: int) -> List[Dict[str, Any]]:
    """Devolver todas las reseñas de un libro ordenadas por fecha de creación."""

    collection = get_reviews_collection()
    documents = list(collection.find({"book_id": book_id}))
    documents.sort(key=lambda doc: doc.get("created_at", ""), reverse=True)
    return [_serialize_review(doc) for doc in documents]


def get_average_rating_for_book(book_id: int) -> Tuple[float | None, int]:
    """Calcular la media de rating y el número de reseñas de un libro."""

    collection = get_reviews_collection()
    ratings: List[int] = []
    for document in collection.find({"book_id": book_id}):
        rating_value = document.get("rating")
        if isinstance(rating_value, (int, float)):
            ratings.append(int(rating_value))
    total_reviews = len(ratings)
    if not total_reviews:
        return None, 0
    average = sum(ratings) / total_reviews
    return round(average, 2), total_reviews


def _normalize_rating(value: int | str) -> int:
    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValueError("El rating es obligatorio")
        if value.isdigit():
            value = int(value)
        else:
            raise ValueError("El rating debe ser un número entero")
    if not isinstance(value, int):
        raise ValueError("El rating debe ser un número entero")
    if value < 1 or value > 5:
        raise ValueError("El rating debe estar entre 1 y 5")
    return value


def _normalize_comment(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("El comentario debe ser texto")
    normalized = value.strip()
    return normalized or None


def _serialize_review(document: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(document.get("_id")),
        "book_id": document.get("book_id"),
        "user_id": document.get("user_id"),
        "username": document.get("username"),
        "rating": document.get("rating"),
        "comment": document.get("comment"),
        "created_at": document.get("created_at"),
        "updated_at": document.get("updated_at"),
    }
