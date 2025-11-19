"""Tests asociados al Trabajo6 (usuarios y permisos en la API)."""
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


def _make_user(username: str = "permisos-user") -> User:
    return User.objects.create_user(username=username, password="segura")


def test_trabajo06_listado_books_anonymous_devuelve_200():
    BookRepository.create(title="Libre", author="Publico")

    response = _call("/api/books/", method="GET")

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert isinstance(payload, list)


def test_trabajo06_detalle_book_anonymous_devuelve_200():
    book = BookRepository.create(title="Disponible", author="Alguien")

    response = _call(f"/api/books/{book.id}/", method="GET")

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["id"] == book.id


def test_trabajo06_crear_book_anonymous_devuelve_401():
    response = _call(
        "/api/books/",
        method="POST",
        body={"title": "Prohibido", "author": "Anon"},
    )

    assert response.status_code == 401
    assert not BookRepository.list_all()


def test_trabajo06_crear_book_autenticado_devuelve_201():
    user = _make_user()

    response = _call(
        "/api/books/",
        method="POST",
        body={"title": "Permitido", "author": "Admin"},
        user=user,
    )

    assert response.status_code == 201
    payload = json.loads(response.content)
    assert payload["created_by"] == user.username


def test_trabajo06_actualizar_book_anonymous_devuelve_401():
    book = BookRepository.create(title="Viejo", author="Autor")

    response = _call(
        f"/api/books/{book.id}/",
        method="PATCH",
        body={"title": "Nuevo"},
    )

    assert response.status_code == 401
    assert BookRepository.get(book.id).title == "Viejo"


def test_trabajo06_actualizar_book_autenticado_devuelve_200():
    book = BookRepository.create(title="Viejo", author="Autor")
    user = _make_user()

    response = _call(
        f"/api/books/{book.id}/",
        method="PATCH",
        body={"title": "Nuevo"},
        user=user,
    )

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["title"] == "Nuevo"


def test_trabajo06_borrar_book_anonymous_devuelve_401():
    book = BookRepository.create(title="Para borrar", author="Autor")

    response = _call(f"/api/books/{book.id}/", method="DELETE")

    assert response.status_code == 401
    assert BookRepository.get(book.id).id == book.id


def test_trabajo06_borrar_book_autenticado_devuelve_204():
    book = BookRepository.create(title="Para borrar", author="Autor")
    user = _make_user()

    response = _call(f"/api/books/{book.id}/", method="DELETE", user=user)

    assert response.status_code == 204
    assert not BookRepository.list_all()
