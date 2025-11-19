"""Tests asociados al Trabajo10 (Neo4j + Celery + recomendaciones)."""
from __future__ import annotations

import json
import os

import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.urls import resolve

from library.models import BookRepository
from library.neo4j_client import get_neo4j_driver
from library.neo4j_service import (
    get_graph_snapshot,
    get_recommended_books_for_user,
    reset_graph_state,
    sync_book_node,
    sync_review_relation,
    sync_user_node,
)
from library.reviews_service import create_review, get_reviews_collection
from library.tasks import (
    task_sync_book_reviews_to_neo4j,
    task_sync_user_recommendations,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
if not settings.configured:
    django.setup()


def setup_function(_: object) -> None:
    BookRepository.reset()
    User.objects.reset()
    get_reviews_collection().delete_many({})
    reset_graph_state()


def _call(path: str, *, method: str = "GET", body: dict | None = None, user: User | None = None):
    route = resolve(path)
    request = HttpRequest()
    request.method = method.upper()
    request.path = path
    request.user = user or AnonymousUser()
    request.body = b"" if request.method == "GET" else json.dumps(body or {}).encode("utf-8")
    return route.callback(request, **route.kwargs)


def _make_user(username: str) -> User:
    return User.objects.create_user(username=username, password="segura")


def test_trabajo10_settings_incluyen_neo4j_y_celery():
    assert getattr(settings, "NEO4J_URI", None)
    assert getattr(settings, "NEO4J_USER", None)
    assert getattr(settings, "NEO4J_PASSWORD", None)
    assert getattr(settings, "CELERY_BROKER_URL", None)
    assert getattr(settings, "CELERY_RESULT_BACKEND", None)


def test_trabajo10_get_neo4j_driver_devuelve_driver():
    driver = get_neo4j_driver()
    session = driver.session()
    assert hasattr(driver, "session")
    assert hasattr(session, "run")


def test_trabajo10_task_sync_book_reviews_crea_nodos_y_relaciones():
    book = BookRepository.create(title="Neo4j", author="Graph")
    user = _make_user("grafo-user")
    create_review(book_id=book.id, user_id=user.id, username=user.username, rating=5, comment="Top")

    payload = task_sync_book_reviews_to_neo4j(book.id)

    snapshot = get_graph_snapshot()
    assert payload["reviews_synced"] == 1
    assert book.id in snapshot["books"]
    assert user.id in snapshot["users"]
    assert user.id in snapshot["ratings"].get(book.id, {})


def test_trabajo10_recommendations_autenticado_devuelve_lista():
    reviewer = _make_user("reviewer")
    target = _make_user("lector")
    book_a = BookRepository.create(title="Libro A", author="Autora")
    book_b = BookRepository.create(title="Libro B", author="Autor")
    create_review(book_id=book_a.id, user_id=reviewer.id, username=reviewer.username, rating=5, comment="Genial")
    create_review(book_id=book_b.id, user_id=reviewer.id, username=reviewer.username, rating=4, comment="Bien")
    create_review(book_id=book_a.id, user_id=target.id, username=target.username, rating=5, comment="Lo mismo")

    task_sync_book_reviews_to_neo4j(book_a.id)
    task_sync_book_reviews_to_neo4j(book_b.id)

    response = _call("/api/recommendations/", user=target)

    assert response.status_code == 200
    payload = json.loads(response.content)
    assert isinstance(payload, list)
    assert payload and payload[0]["book_id"] == book_b.id


def test_trabajo10_recommendations_anonymous_devuelve_401():
    response = _call("/api/recommendations/")
    assert response.status_code == 401


def test_trabajo10_task_sync_user_recommendations_devuelve_lista():
    reviewer = _make_user("reviewer2")
    target = _make_user("lector2")
    book_a = BookRepository.create(title="Aprender Neo4j", author="Doc")
    book_b = BookRepository.create(title="Profundizar", author="Doc")
    create_review(book_id=book_a.id, user_id=reviewer.id, username=reviewer.username, rating=5, comment="Top")
    create_review(book_id=book_b.id, user_id=reviewer.id, username=reviewer.username, rating=4, comment="Nice")
    create_review(book_id=book_a.id, user_id=target.id, username=target.username, rating=4, comment="Bien")

    task_sync_book_reviews_to_neo4j(book_a.id)
    task_sync_book_reviews_to_neo4j(book_b.id)

    result = task_sync_user_recommendations(target.id, limit=5)

    assert isinstance(result, list)
    assert result and result[0]["book_id"] == book_b.id


def test_trabajo10_sync_helpers_pueden_usarse_directamente():
    book = BookRepository.create(title="Manual", author="Experta")
    user = _make_user("grafo-directo")

    sync_book_node(book)
    sync_user_node(user)
    sync_review_relation(book_id=book.id, user_id=user.id, rating=4)

    recommendations = get_recommended_books_for_user(user.id)
    assert recommendations == []
