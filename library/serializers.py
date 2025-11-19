"""Serializers for API payloads."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping

from .models import Book


class BookSerializer:
    """Serialize Book instances to primitives apt for JSON."""

    fields = ("id", "title", "author", "published_year", "isbn", "created_by")

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


class BookInputSerializer:
    """Validate incoming payloads for creation and updates."""

    required_fields = ("title", "author")
    optional_fields = ("published_year", "isbn")
    allowed_fields = required_fields + optional_fields

    def __init__(self, data: Mapping[str, Any] | None, *, partial: bool = False) -> None:
        self.data: Dict[str, Any] = dict(data or {})
        self.partial = partial
        self._errors: Dict[str, List[str]] = {}
        self.validated_data: Dict[str, Any] = {}

    def is_valid(self) -> bool:
        cleaned: Dict[str, Any] = {}
        self._errors = {}
        for field in self.allowed_fields:
            if field not in self.data:
                continue
            valid, normalized = self._validate_field(field, self.data[field])
            if valid:
                cleaned[field] = normalized
        for field in self.required_fields:
            if field not in cleaned:
                if self.partial and field not in self.data:
                    continue
                self._errors.setdefault(field, []).append("Este campo es obligatorio.")
        if not self._errors:
            self.validated_data = cleaned
        else:
            self.validated_data = {}
        return not self._errors

    @property
    def errors(self) -> Dict[str, List[str]]:
        return self._errors

    def _validate_field(self, field: str, value: Any) -> tuple[bool, Any]:
        if field in {"title", "author", "isbn"}:
            if value is None:
                if field in self.required_fields:
                    self._errors.setdefault(field, []).append("Este campo es obligatorio.")
                    return False, None
                return True, None
            if not isinstance(value, str):
                self._errors.setdefault(field, []).append("Debe ser una cadena.")
                return False, None
            normalized = value.strip()
            if field in self.required_fields and not normalized:
                self._errors.setdefault(field, []).append("Este campo es obligatorio.")
                return False, None
            if field == "isbn" and not normalized:
                return True, None
            return True, normalized
        if field == "published_year":
            if value in (None, ""):
                return True, None
            if isinstance(value, int):
                return True, value
            if isinstance(value, str) and value.strip().isdigit():
                return True, int(value.strip())
            self._errors.setdefault(field, []).append("Debe ser un número entero.")
            return False, None
        return True, value
