"""Tests asociados al Trabajo5 (CRUD completo de libros)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.urls import resolve

from library.models import BookRepository

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def setup_function(_: object) -> None:
    BookRepository.reset()
    User.objects.reset()


def _call(path: str, *, method: str, body: dict | None = None, user: User | None = None):
    route = resolve(path)
    payload = json.dumps(body or {}).encode("utf-8") if method.upper() != "GET" else None
    request = HttpRequest(
        method=method.upper(),
        path=path,
        body=payload,
        user=user or AnonymousUser(),
    )
    return route.callback(request, **route.kwargs)


def _make_user(username: str = "api-user") -> User:
    return User.objects.create_user(username=username, password="segura")


def test_trabajo05_crear_book_valido_devuelve_201():
    response = _call(
        "/api/books/",
        method="POST",
        body={"title": "Nuevo libro", "author": "Autora", "published_year": 2024},
        user=_make_user(),
    )

    assert response.status_code == 201
    payload = json.loads(response.content)
    assert payload["title"] == "Nuevo libro"
    assert payload["created_by"] == "api-user"
    assert len(BookRepository.list_all()) == 1


def test_trabajo05_crear_book_sin_titulo_devuelve_400():
    response = _call(
        "/api/books/",
        method="POST",
        body={"author": "Autor"},
        user=_make_user("invalid-user"),
    )

    assert response.status_code == 400
    payload = json.loads(response.content)
    assert "title" in payload["errors"]


def test_trabajo05_actualizar_book_valido_devuelve_200():
    book = BookRepository.create(title="Título", author="Autor")

    response = _call(
        f"/api/books/{book.id}/",
        method="PUT",
        body={"title": "Actualizado", "author": "Autor 2"},
        user=_make_user(),
    )

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["title"] == "Actualizado"
    assert BookRepository.get(book.id).title == "Actualizado"


def test_trabajo05_actualizar_book_invalido_devuelve_400():
    book = BookRepository.create(title="Título", author="Autor")

    response = _call(
        f"/api/books/{book.id}/",
        method="PATCH",
        body={"title": ""},
        user=_make_user(),
    )

    assert response.status_code == 400
    payload = json.loads(response.content)
    assert "title" in payload["errors"]


def test_trabajo05_borrar_book_existente_devuelve_204():
    book = BookRepository.create(title="Título", author="Autor")

    response = _call(f"/api/books/{book.id}/", method="DELETE", user=_make_user())

    assert response.status_code == 204
    assert not BookRepository.list_all()


def test_trabajo05_borrar_book_inexistente_devuelve_404():
    response = _call("/api/books/999/", method="DELETE", user=_make_user())

    assert response.status_code == 404
    payload = json.loads(response.content)
    assert payload["detail"].lower().startswith("libro")
