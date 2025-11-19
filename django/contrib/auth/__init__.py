"""Lightweight helpers mirroring django.contrib.auth."""
from __future__ import annotations

from typing import Any, Optional

from .models import AnonymousUser, User


def get_user_model() -> type[User]:  # pragma: no cover - trivial
    return User


def authenticate(*, username: Optional[str] = None, password: Optional[str] = None) -> User | None:
    for user in User.objects.all():
        if user.username == username and user.check_password(password):
            return user
    return None


def login(request: Any, user: User) -> None:  # pragma: no cover - trivial helper
    if request is not None:
        request.user = user


def logout(request: Any) -> None:  # pragma: no cover - trivial helper
    if request is not None:
        request.user = AnonymousUser()


__all__ = ["authenticate", "login", "logout", "get_user_model", "User", "AnonymousUser"]
