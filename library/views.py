"""Views for the principal Biblioteca app."""
from __future__ import annotations

from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponse


def health(request: HttpRequest | None = None) -> HttpResponse:
    """Return a lightweight health indicator."""
    timestamp = datetime.now(tz=UTC).isoformat(timespec="seconds")
    message = f"Biblioteca Online activa - {timestamp}"
    return HttpResponse(message, status=200)
