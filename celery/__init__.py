"""Minimal Celery stub used for offline testing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass
class EagerResult:
    """Simple object that mimics the result returned by Celery."""

    value: Any

    def get(self, timeout: int | None = None) -> Any:  # pragma: no cover - trivial proxy
        return self.value


class Celery:
    """Very small subset of Celery's API to register and call tasks synchronously."""

    def __init__(self, main: str) -> None:
        self.main = main
        self.conf: Dict[str, Any] = {}
        self._tasks: Dict[str, Callable[..., Any]] = {}

    def task(self, name: str | None = None, **_: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator compatible with @app.task."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            task_name = name or func.__name__
            self._tasks[task_name] = func

            def delay(*args: Any, **kwargs: Any) -> EagerResult:
                return EagerResult(func(*args, **kwargs))

            def apply_async(
                args: tuple[Any, ...] | None = None,
                kwargs: Dict[str, Any] | None = None,
            ) -> EagerResult:
                return EagerResult(func(*(args or ()), **(kwargs or {})))

            func.delay = delay  # type: ignore[attr-defined]
            func.apply_async = apply_async  # type: ignore[attr-defined]
            return func

        return decorator


__all__ = ["Celery"]
