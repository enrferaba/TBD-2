"""Utilities to keep an in-memory Neo4j graph in sync for tests."""
from __future__ import annotations

from typing import Dict, List, Tuple

from django.contrib.auth.models import User

from .models import Book
from .neo4j_client import get_neo4j_driver


def _graph_state() -> Dict[str, Dict]:
    driver = get_neo4j_driver()
    state = getattr(driver, "_graph_state", None)
    if state is None:
        state = {"books": {}, "users": {}, "ratings": {}}
        driver._graph_state = state  # type: ignore[attr-defined]
    return state


def reset_graph_state() -> None:
    """Utility for tests so every scenario starts from a clean graph."""

    state = _graph_state()
    state["books"].clear()
    state["users"].clear()
    state["ratings"].clear()


def get_graph_snapshot() -> Dict[str, Dict]:
    """Return a shallow copy of the graph for assertions."""

    state = _graph_state()
    return {
        "books": dict(state["books"]),
        "users": dict(state["users"]),
        "ratings": {book_id: dict(ratings) for book_id, ratings in state["ratings"].items()},
    }


def sync_book_node(book: Book) -> Dict[str, object]:
    state = _graph_state()
    payload = {"id": book.id, "title": book.title, "author": book.author}
    state["books"][book.id] = payload
    return payload


def sync_user_node(user: User) -> Dict[str, object]:
    state = _graph_state()
    payload = {"id": user.id, "username": user.username}
    state["users"][user.id] = payload
    return payload


def sync_review_relation(*, book_id: int, user_id: int, rating: int) -> Tuple[int, int]:
    state = _graph_state()
    ratings = state["ratings"].setdefault(book_id, {})
    ratings[user_id] = int(rating)
    return book_id, user_id


def get_recommended_books_for_user(user_id: int, limit: int = 5) -> List[Dict[str, object]]:
    state = _graph_state()
    rated_by_user = {
        book_id for book_id, user_ratings in state["ratings"].items() if user_id in user_ratings
    }
    candidates: List[Dict[str, object]] = []
    for book_id, book in state["books"].items():
        if book_id in rated_by_user:
            continue
        ratings = state["ratings"].get(book_id)
        if not ratings:
            continue
        average = sum(ratings.values()) / len(ratings)
        candidates.append(
            {
                "book_id": book_id,
                "title": book["title"],
                "author": book["author"],
                "average_rating": round(average, 2),
                "num_reviews": len(ratings),
            }
        )
    candidates.sort(key=lambda item: (item["average_rating"], item["num_reviews"]), reverse=True)
    return candidates[:limit]
