import importlib
import os

import django
from django.conf import settings


def ensure_django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
    if not settings.configured:
        django.setup()


def test_settings_module_is_importable():
    module = importlib.import_module("biblioteca_config.settings")
    assert hasattr(module, "DEBUG")
    assert module.BASE_DIR.name == "TBD-2"


def test_debug_flag_is_boolean():
    ensure_django_setup()
    assert isinstance(settings.DEBUG, bool)
