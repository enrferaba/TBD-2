"""API views for the Biblioteca Online project."""
from __future__ import annotations

from typing import Any, Dict

from rest_framework import APIView, Response


class HealthAPIView(APIView):
    """Return a JSON payload confirming the service status."""

    def get(self, request: Any | None = None) -> Response:
        payload: Dict[str, str] = {
            "service": "Biblioteca Online",
            "status": "ok",
            "version": "trabajo3",
        }
        return Response(payload, status=200)
