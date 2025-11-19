"""Ligera implementación en memoria compatible con PyMongo para tests."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Mapping, MutableMapping, Optional
from urllib.parse import urlparse


@dataclass
class InsertOneResult:
    """Resultado simplificado de insert_one."""

    inserted_id: Any


@dataclass
class DeleteResult:
    """Resultado simplificado de delete_many."""

    deleted_count: int


class _AdminModule:
    """Soporta comandos básicos como `ping`."""

    def __init__(self, client: "MongoClient") -> None:
        self._client = client

    def command(self, name: str, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        if name == "ping":
            return {"ok": 1}
        raise NotImplementedError(f"Comando {name} no soportado en el stub de PyMongo")


class Collection:
    """Colección en memoria con una API inspirada en PyMongo."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._documents: List[Dict[str, Any]] = []
        self._next_id = 1

    def _match(self, document: Mapping[str, Any], filtro: Optional[Mapping[str, Any]]) -> bool:
        if not filtro:
            return True
        for field, value in filtro.items():
            if document.get(field) != value:
                return False
        return True

    def insert_one(self, document: MutableMapping[str, Any]) -> InsertOneResult:
        payload = dict(document)
        payload.setdefault("_id", self._next_id)
        self._next_id += 1
        self._documents.append(payload)
        return InsertOneResult(payload["_id"])

    def find(self, filtro: Optional[Mapping[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        for document in list(self._documents):
            if self._match(document, filtro):
                yield dict(document)

    def find_one(self, filtro: Optional[Mapping[str, Any]] = None) -> Optional[Dict[str, Any]]:
        for document in self.find(filtro):
            return document
        return None

    def delete_many(self, filtro: Optional[Mapping[str, Any]] = None) -> DeleteResult:
        before = len(self._documents)
        self._documents = [doc for doc in self._documents if not self._match(doc, filtro)]
        return DeleteResult(deleted_count=before - len(self._documents))

    def count_documents(self, filtro: Optional[Mapping[str, Any]] = None) -> int:
        return sum(1 for _ in self.find(filtro))


class Database:
    """Base de datos en memoria que agrupa colecciones."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._collections: Dict[str, Collection] = {}

    def __getitem__(self, name: str) -> Collection:
        if name not in self._collections:
            self._collections[name] = Collection(name)
        return self._collections[name]


class MongoClient:
    """Cliente Mongo minimalista."""

    def __init__(self, uri: Optional[str] = None, **_: Any) -> None:
        self._uri = uri or "mongodb://localhost:27017"
        self._databases: Dict[str, Database] = {}
        self.admin = _AdminModule(self)
        parsed = urlparse(self._uri)
        default_db = parsed.path.lstrip("/") if parsed.path else ""
        self._default_db = default_db or None

    def __getitem__(self, name: str) -> Database:
        if name not in self._databases:
            self._databases[name] = Database(name)
        return self._databases[name]

    def get_default_database(self) -> Database:
        if not self._default_db:
            raise ValueError("La URI no define una base de datos por defecto")
        return self[self._default_db]

    def get_database(self, name: Optional[str] = None) -> Database:
        if name is None:
            return self.get_default_database()
        return self[name]

    def close(self) -> None:  # pragma: no cover - API parity
        return None

    def server_info(self) -> Dict[str, Any]:
        return {"version": "fake-pymongo"}


__all__ = [
    "Collection",
    "Database",
    "DeleteResult",
    "InsertOneResult",
    "MongoClient",
]
