"""Celery tasks for keeping the Neo4j graph and recommendations fresh."""
from __future__ import annotations

from typing import Dict, List

from django.contrib.auth.models import User

from . import celery_app
from .models import BookRepository
from .neo4j_service import (
    get_recommended_books_for_user,
    sync_book_node,
    sync_review_relation,
    sync_user_node,
)
from .reviews_service import get_reviews_for_book


def _find_user(user_id: int, username: str | None) -> User:
    for candidate in User.objects.all():
        if candidate.id == user_id:
            return candidate
    user = User(username=username or f"user-{user_id}")
    user.id = user_id
    return user


@celery_app.task(name="library.task_sync_book_reviews_to_neo4j")
def task_sync_book_reviews_to_neo4j(book_id: int) -> Dict[str, int]:
    """Synchronize book, user nodes and relations based on Mongo reviews."""

    try:
        book = BookRepository.get(book_id)
    except LookupError:
        return {"book_id": book_id, "reviews_synced": 0}
    sync_book_node(book)
    reviews = get_reviews_for_book(book_id)
    synced = 0
    for review in reviews:
        user = _find_user(review.get("user_id", 0), review.get("username"))
        sync_user_node(user)
        sync_review_relation(book_id=book_id, user_id=user.id, rating=review.get("rating", 0))
        synced += 1
    return {"book_id": book_id, "reviews_synced": synced}


@celery_app.task(name="library.task_sync_user_recommendations")
def task_sync_user_recommendations(user_id: int, limit: int = 5) -> List[Dict[str, object]]:
    """Return the recommended books for a given user."""

    return get_recommended_books_for_user(user_id, limit=limit)
