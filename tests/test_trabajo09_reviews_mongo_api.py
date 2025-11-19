"""Tests asociados al Trabajo9 (reseñas y valoraciones en MongoDB)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.urls import resolve

from library.models import BookRepository
from library.reviews_service import (
    create_review,
    get_average_rating_for_book,
    get_reviews_collection,
    get_reviews_for_book,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def setup_function(_: object) -> None:
    BookRepository.reset()
    User.objects.reset()
    get_reviews_collection().delete_many({})


def _call(path: str, *, method: str = "GET", body: dict | None = None, user: User | None = None):
    route = resolve(path)
    request = HttpRequest()
    request.method = method.upper()
    request.path = path
    request.user = user or AnonymousUser()
    if request.method == "GET":
        request.body = b""
    else:
        request.body = json.dumps(body or {}).encode("utf-8")
    return route.callback(request, **route.kwargs)


def _make_user(username: str = "reviews-user") -> User:
    return User.objects.create_user(username=username, password="segura")


def test_trabajo09_create_review_inserta_documento_en_mongo():
    book = BookRepository.create(title="Mongo", author="Tester")
    user = _make_user()

    review = create_review(book_id=book.id, user_id=user.id, username=user.username, rating=5, comment="Genial")

    collection = get_reviews_collection()
    assert collection.count_documents({"book_id": book.id}) == 1
    assert review["rating"] == 5
    assert review["username"] == user.username


def test_trabajo09_get_reviews_for_book_devuelve_lista_correcta():
    book = BookRepository.create(title="Libro", author="Autora")
    otro = BookRepository.create(title="Otro", author="Autor")
    user = _make_user()

    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=4, comment="Bien")
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=3, comment="Ok")
    create_review(book_id=otro.id, user_id=user.id, username=user.username, rating=1, comment="Mal")

    reviews = get_reviews_for_book(book.id)

    assert len(reviews) == 2
    assert all(review["book_id"] == book.id for review in reviews)


def test_trabajo09_get_average_rating_for_book_calcula_media():
    book = BookRepository.create(title="Promedio", author="Autor")
    user = _make_user()

    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=5, comment="Top")
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=3, comment="Medio")

    average, total = get_average_rating_for_book(book.id)

    assert average == 4.0
    assert total == 2


def test_trabajo09_listado_reviews_book_devuelve_200_y_lista():
    book = BookRepository.create(title="API", author="Cliente")
    user = _make_user()
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=4, comment="Nice")

    response = _call(f"/api/books/{book.id}/reviews/", method="GET")

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert isinstance(payload, list)
    assert payload[0]["book_id"] == book.id


def test_trabajo09_crear_review_autenticado_devuelve_201():
    book = BookRepository.create(title="CRUD", author="API")
    user = _make_user()

    response = _call(
        f"/api/books/{book.id}/reviews/",
        method="POST",
        user=user,
        body={"rating": 4, "comment": "Correcta"},
    )

    assert response.status_code == 201
    payload = json.loads(response.content)
    assert payload["rating"] == 4
    assert payload["username"] == user.username


def test_trabajo09_crear_review_anonymous_devuelve_401():
    book = BookRepository.create(title="Seguridad", author="API")

    response = _call(
        f"/api/books/{book.id}/reviews/",
        method="POST",
        body={"rating": 5, "comment": "Sin login"},
    )

    assert response.status_code == 401
    assert get_reviews_collection().count_documents({}) == 0


def test_trabajo09_crear_review_rating_fuera_de_rango_devuelve_400():
    book = BookRepository.create(title="Validación", author="API")
    user = _make_user()

    response = _call(
        f"/api/books/{book.id}/reviews/",
        method="POST",
        user=user,
        body={"rating": 10, "comment": "Exagerado"},
    )

    assert response.status_code == 400
    payload = json.loads(response.content)
    assert "rating" in payload["errors"]


def test_trabajo09_endpoint_rating_devuelve_media_correcta():
    book = BookRepository.create(title="Rating", author="API")
    user = _make_user()
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=5, comment="Excelente")
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=3, comment="Mejorable")

    response = _call(f"/api/books/{book.id}/rating/", method="GET")

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert payload["average_rating"] == 4.0
    assert payload["num_reviews"] == 2
