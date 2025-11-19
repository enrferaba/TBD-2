"""URL mappings for the Biblioteca Online API."""
from __future__ import annotations

from django.urls import path

from . import api

app_name = "library_api"

urlpatterns = [
    path("api/health/", api.HealthAPIView.as_view(), name="api-health"),
]
