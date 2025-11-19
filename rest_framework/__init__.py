"""Minimal subset of Django REST Framework used in tests."""
from .response import Response
from .views import APIView

__all__ = ["Response", "APIView"]
