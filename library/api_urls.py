"""URL mappings for the Biblioteca Online API."""
from __future__ import annotations

from django.urls import path

from . import api

app_name = "library_api"

urlpatterns = [
    path("api/health/", api.HealthAPIView.as_view(), name="api-health"),
    path("api/books/", api.BookListAPIView.as_view(), name="api-books-list"),
    path(
        "api/books/<int:book_id>/",
        api.BookDetailAPIView.as_view(),
        name="api-books-detail",
    ),
]
