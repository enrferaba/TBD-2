import importlib
import os

import django
from django.conf import settings


def ensure_django_setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca_config.settings")
    if not settings.configured:
        django.setup()


def test_trabajo01_settings_module_es_importable():
    module = importlib.import_module("biblioteca_config.settings")
    assert hasattr(module, "DEBUG")
    assert module.BASE_DIR.name == "TBD-2"


def test_trabajo01_debug_flag_es_booleano():
    ensure_django_setup()
    assert isinstance(settings.DEBUG, bool)
