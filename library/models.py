"""Domain models for the Biblioteca Online project."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import ClassVar, Dict, Iterable, List


@dataclass(slots=True)
class Book:
    """Minimal representation of a book entry."""

    title: str
    author: str
    published_year: int | None = None
    isbn: str | None = None
    id: int = field(init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

    def __post_init__(self) -> None:
        timestamp = datetime.now(tz=UTC)
        self.created_at = timestamp
        self.updated_at = timestamp


class BookRepository:
    """In-memory repository that simulates ORM persistence for tests."""

    _records: ClassVar[Dict[int, Book]] = {}
    _next_id: ClassVar[int] = 1

    @classmethod
    def create(
        cls,
        *,
        title: str,
        author: str,
        published_year: int | None = None,
        isbn: str | None = None,
    ) -> Book:
        book = Book(title=title, author=author, published_year=published_year, isbn=isbn)
        book.id = cls._next_id
        cls._next_id += 1
        cls._records[book.id] = book
        return book

    @classmethod
    def list_all(cls) -> List[Book]:
        return sorted(cls._records.values(), key=lambda book: book.id)

    @classmethod
    def get(cls, book_id: int) -> Book:
        try:
            return cls._records[book_id]
        except KeyError as exc:  # pragma: no cover - defensive programming
            raise LookupError(f"Book {book_id} not found") from exc

    @classmethod
    def replace_all(cls, books: Iterable[Book]) -> None:
        cls._records = {book.id: book for book in books}
        cls._next_id = (max(cls._records) + 1) if cls._records else 1

    @classmethod
    def reset(cls) -> None:
        cls._records = {}
        cls._next_id = 1
