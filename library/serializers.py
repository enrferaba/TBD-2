"""Serializers for API payloads."""
from __future__ import annotations

from typing import Iterable, List

from .models import Book


class BookSerializer:
    """Serialize Book instances to primitives apt for JSON."""

    fields = ("id", "title", "author", "published_year", "isbn")

    def __init__(self, instance: Book | Iterable[Book], *, many: bool = False) -> None:
        self.instance = instance
        self.many = many

    def data(self) -> List[dict] | dict:
        if self.many:
            books = list(self.instance) if not isinstance(self.instance, list) else self.instance
            return [self._serialize(book) for book in books]
        return self._serialize(self.instance)  # type: ignore[arg-type]

    def _serialize(self, book: Book) -> dict:
        return {field: getattr(book, field) for field in self.fields}
