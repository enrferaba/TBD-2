"""Tests asociados al Trabajo4 (modelo y API de libros)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.http import HttpRequest
from django.urls import resolve

from library.models import BookRepository

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def setup_function(_: object) -> None:
    BookRepository.reset()


def test_trabajo04_listado_books_responde_200():
    BookRepository.create(title="Libro 1", author="Autor 1", published_year=2020)
    BookRepository.create(title="Libro 2", author="Autor 2", published_year=2021)

    route = resolve("/api/books/")
    response = route.callback(HttpRequest(path="/api/books/"))

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert isinstance(payload, list)
    assert len(payload) == 2
    assert {entry["title"] for entry in payload} == {"Libro 1", "Libro 2"}


def test_trabajo04_detalle_book_responde_200():
    book = BookRepository.create(title="Libro Único", author="Autora", published_year=2019)

    route = resolve(f"/api/books/{book.id}/")
    response = route.callback(HttpRequest(path=f"/api/books/{book.id}/"), **route.kwargs)

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["id"] == book.id
    assert payload["title"] == "Libro Único"
    assert payload["author"] == "Autora"


def test_trabajo04_detalle_book_inexistente_responde_404():
    route = resolve("/api/books/999/")
    response = route.callback(HttpRequest(path="/api/books/999/"), **route.kwargs)

    assert response.status_code == 404
    payload = json.loads(response.content)
    assert payload["detail"].lower().startswith("libro")
