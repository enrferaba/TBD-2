"""Very small authentication models subset for tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, List


class UserManager:
    """In-memory replacement for Django's user manager."""

    def __init__(self) -> None:
        self._storage: List[User] = []
        self._next_id = 1

    def create_user(self, username: str, password: str | None = None, **extra: Any) -> User:
        user = User(username=username, **extra)
        user.id = self._next_id
        self._next_id += 1
        user.set_password(password or "")
        self._storage.append(user)
        return user

    def all(self) -> List[User]:
        return list(self._storage)

    def reset(self) -> None:
        self._storage = []
        self._next_id = 1


@dataclass
class User:
    """Simple user model compatible with the tests."""

    username: str
    password: str = field(repr=False, default="")
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True
    id: int = field(init=False, default=0)

    objects: ClassVar[UserManager] = UserManager()

    def set_password(self, raw_password: str) -> None:
        self.password = raw_password

    def check_password(self, raw_password: str | None) -> bool:
        return self.password == (raw_password or "")

    @property
    def is_authenticated(self) -> bool:  # pragma: no cover - trivial
        return True


class AnonymousUser:
    """Anonymous placeholder used for unauthenticated requests."""

    username = None
    is_staff = False
    is_superuser = False
    is_active = False

    @property
    def is_authenticated(self) -> bool:  # pragma: no cover - trivial
        return False


__all__ = ["User", "AnonymousUser"]
