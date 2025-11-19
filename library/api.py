"""API views for the Biblioteca Online project."""
from __future__ import annotations

from typing import Any, Dict

from rest_framework import APIView, Response

from .models import BookRepository
from .serializers import BookSerializer


class HealthAPIView(APIView):
    """Return a JSON payload confirming the service status."""

    def get(self, request: Any | None = None) -> Response:
        payload: Dict[str, str] = {
            "service": "Biblioteca Online",
            "status": "ok",
            "version": "trabajo4",
        }
        return Response(payload, status=200)


class BookListAPIView(APIView):
    """Return every book stored in the repository."""

    def get(self, request: Any | None = None) -> Response:
        serializer = BookSerializer(BookRepository.list_all(), many=True)
        return Response(serializer.data(), status=200)


class BookDetailAPIView(APIView):
    """Return the serialized representation for a single book."""

    def get(self, request: Any | None = None, *, book_id: int) -> Response:
        try:
            book = BookRepository.get(book_id)
        except LookupError:
            return Response({"detail": "Libro no encontrado"}, status=404)
        serializer = BookSerializer(book)
        return Response(serializer.data(), status=200)
