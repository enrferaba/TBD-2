"""URL mappings for the Biblioteca Online API."""
from __future__ import annotations

from django.urls import path

from . import api

app_name = "library_api"

urlpatterns = [
    path("api/health/", api.HealthAPIView.as_view(), name="api-health"),
    path(
        "api/mongo/health/",
        api.MongoHealthAPIView.as_view(),
        name="api-mongo-health",
    ),
    path("api/books/", api.BookListAPIView.as_view(), name="api-books-list"),
    path(
        "api/books/<int:book_id>/",
        api.BookDetailAPIView.as_view(),
        name="api-books-detail",
    ),
    path(
        "api/books/<int:book_id>/reviews/",
        api.BookReviewsAPIView.as_view(),
        name="api-books-reviews",
    ),
    path(
        "api/books/<int:book_id>/rating/",
        api.BookRatingAPIView.as_view(),
        name="api-books-rating",
    ),
    path("api/recommendations/", api.RecommendationsAPIView.as_view(), name="api-recommendations"),
]
