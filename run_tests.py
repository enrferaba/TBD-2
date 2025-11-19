#!/usr/bin/env python
import os
import sys

import pytest


def main() -> int:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
    return pytest.main(["-vv", "tests"])


if __name__ == "__main__":
    raise SystemExit(main())
