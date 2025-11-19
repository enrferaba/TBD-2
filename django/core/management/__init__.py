"""Placeholder for Django's management utilities."""
from __future__ import annotations

import sys


def execute_from_command_line(argv: list[str] | None = None) -> None:
    """Signal clearly that management commands are not available."""
    argv = argv or sys.argv
    command = argv[1] if len(argv) > 1 else "help"
    raise NotImplementedError(
        f"Management command '{command}' is not implemented in this offline stub."
    )


__all__ = ["execute_from_command_line"]
