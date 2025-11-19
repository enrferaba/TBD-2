"""API views for the Biblioteca Online project."""
from __future__ import annotations

import json
from typing import Any, Dict

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework import APIView, Response

from .models import BookRepository
from .mongo_client import get_mongo_client
from .neo4j_service import get_recommended_books_for_user
from .reviews_service import (
    create_review,
    get_average_rating_for_book,
    get_reviews_for_book,
)
from .tasks import task_sync_book_reviews_to_neo4j, task_sync_user_recommendations
from .serializers import BookInputSerializer, BookSerializer


class HealthAPIView(APIView):
    """Return a JSON payload confirming the service status."""

    def get(self, request: Any | None = None) -> Response:
        payload: Dict[str, str] = {
            "service": "Biblioteca Online",
            "status": "ok",
            "version": "trabajo4",
        }
        return Response(payload, status=200)


class MongoHealthAPIView(APIView):
    """Comprueba el estado básico de la conexión a MongoDB."""

    def get(self, request: Any | None = None) -> Response:
        try:
            client = get_mongo_client()
            ping = client.admin.command("ping")
            payload = {
                "mongo_status": "ok" if ping.get("ok") == 1 else "error",
                "server_info": client.server_info(),
            }
            status_code = 200 if payload["mongo_status"] == "ok" else 503
        except Exception as exc:  # pragma: no cover - defensivo
            payload = {"mongo_status": "error", "detail": str(exc)}
            status_code = 503
        return Response(payload, status=status_code)


class BookListAPIView(APIView):
    """Return every book stored in the repository."""

    def get(self, request: Any | None = None) -> Response:
        serializer = BookSerializer(BookRepository.list_all(), many=True)
        return Response(serializer.data(), status=200)

    def post(self, request: HttpRequest | None = None) -> Response:
        user, auth_error = _ensure_authenticated(request)
        if auth_error:
            return auth_error
        try:
            payload = _parse_json_body(request)
        except ValueError:
            return Response({"errors": {"non_field_errors": ["JSON inválido"]}}, status=400)
        serializer = BookInputSerializer(payload)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        book = BookRepository.create(
            created_by=getattr(user, "username", None),
            **serializer.validated_data,
        )
        return Response(BookSerializer(book).data(), status=201)


class BookDetailAPIView(APIView):
    """Return the serialized representation for a single book."""

    def get(self, request: Any | None = None, *, book_id: int) -> Response:
        try:
            book = BookRepository.get(book_id)
        except LookupError:
            return _book_not_found_response()
        serializer = BookSerializer(book)
        payload = serializer.data()
        average, reviews_count = get_average_rating_for_book(book_id)
        payload["average_rating"] = average
        payload["reviews_count"] = reviews_count
        return Response(payload, status=200)

    def put(self, request: HttpRequest | None = None, *, book_id: int) -> Response:
        return self._update(request, book_id, partial=False)

    def patch(self, request: HttpRequest | None = None, *, book_id: int) -> Response:
        return self._update(request, book_id, partial=True)

    def delete(self, request: HttpRequest | None = None, *, book_id: int) -> Response:
        _, auth_error = _ensure_authenticated(request)
        if auth_error:
            return auth_error
        try:
            BookRepository.delete(book_id)
        except LookupError:
            return _book_not_found_response()
        return Response({}, status=204)

    def _update(self, request: HttpRequest | None, book_id: int, *, partial: bool) -> Response:
        _, auth_error = _ensure_authenticated(request)
        if auth_error:
            return auth_error
        try:
            BookRepository.get(book_id)
        except LookupError:
            return _book_not_found_response()
        try:
            payload = _parse_json_body(request)
        except ValueError:
            return Response({"errors": {"non_field_errors": ["JSON inválido"]}}, status=400)
        serializer = BookInputSerializer(payload, partial=partial)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=400)
        book = BookRepository.update(book_id, **serializer.validated_data)
        return Response(BookSerializer(book).data(), status=200)


class BookReviewsAPIView(APIView):
    """Gestiona el listado y creación de reseñas por libro."""

    def get(self, request: Any | None = None, *, book_id: int) -> Response:
        if not _book_exists(book_id):
            return _book_not_found_response()
        reviews = get_reviews_for_book(book_id)
        return Response(reviews, status=200)

    def post(self, request: HttpRequest | None = None, *, book_id: int) -> Response:
        user, auth_error = _ensure_authenticated(request)
        if auth_error:
            return auth_error
        if not _book_exists(book_id):
            return _book_not_found_response()
        try:
            payload = _parse_json_body(request)
        except ValueError:
            return Response({"errors": {"non_field_errors": ["JSON inválido"]}}, status=400)
        if "rating" not in payload:
            return Response({"errors": {"rating": ["Este campo es obligatorio."]}}, status=400)
        try:
            review = create_review(
                book_id=book_id,
                user_id=getattr(user, "id", 0),
                username=getattr(user, "username", None),
                rating=payload.get("rating"),
                comment=payload.get("comment"),
            )
        except ValueError as exc:
            return Response({"errors": {"rating": [str(exc)]}}, status=400)
        task_sync_book_reviews_to_neo4j.delay(book_id)
        user_id = getattr(user, "id", 0)
        if user_id:
            task_sync_user_recommendations.delay(user_id)
        return Response(review, status=201)


class BookRatingAPIView(APIView):
    """Devuelve la media de valoración y el número de reseñas de un libro."""

    def get(self, request: Any | None = None, *, book_id: int) -> Response:
        if not _book_exists(book_id):
            return _book_not_found_response()
        average, total = get_average_rating_for_book(book_id)
        payload = {"book_id": book_id, "average_rating": average, "num_reviews": total}
        return Response(payload, status=200)


class RecommendationsAPIView(APIView):
    """Return recommended books for the authenticated user."""

    def get(self, request: HttpRequest | None = None) -> Response:
        user, auth_error = _ensure_authenticated(request)
        if auth_error:
            return auth_error
        recommendations = get_recommended_books_for_user(getattr(user, "id", 0))
        return Response(recommendations, status=200)


def _parse_json_body(request: HttpRequest | None) -> Dict[str, Any]:
    if request is None or getattr(request, "body", None) in (None, b"", ""):
        return {}
    raw_body = request.body
    if isinstance(raw_body, str):
        raw_body = raw_body.encode("utf-8")
    try:
        return json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive programming
        raise ValueError("Invalid JSON") from exc


def _book_not_found_response() -> Response:
    return Response({"detail": "Libro no encontrado"}, status=404)


def _book_exists(book_id: int) -> bool:
    try:
        BookRepository.get(book_id)
        return True
    except LookupError:
        return False


def _ensure_authenticated(request: HttpRequest | None) -> tuple[object, Response | None]:
    user = _request_user(request)
    if not getattr(user, "is_authenticated", False):
        return user, Response({"detail": "Autenticación requerida"}, status=401)
    return user, None


def _request_user(request: HttpRequest | None) -> object:
    if request is None:
        return AnonymousUser()
    user = getattr(request, "user", None)
    return user if user is not None else AnonymousUser()
