"""Helpers to work with the Neo4j driver."""
from __future__ import annotations

from django.conf import settings
from neo4j import GraphDatabase

_driver = None


def get_neo4j_driver():
    """Return (and cache) the Neo4j driver instance."""

    global _driver
    if _driver is None:
        uri = getattr(settings, "NEO4J_URI", "bolt://neo4j:7687")
        user = getattr(settings, "NEO4J_USER", "neo4j")
        password = getattr(settings, "NEO4J_PASSWORD", "secret")
        _driver = GraphDatabase.driver(uri, auth=(user, password))
    return _driver


def get_neo4j_session():
    """Expose a helper for callers that want a raw session."""

    return get_neo4j_driver().session()
