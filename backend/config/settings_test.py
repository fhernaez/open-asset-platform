"""Test settings: override the database with SQLite (a test double).

Unit tests never run against PostgreSQL; integration tests exercise the real
PostgreSQL/TimescaleDB stack via Docker (see scripts/gates).
"""

from __future__ import annotations

from .settings import *  # noqa: F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "test.sqlite3"),  # noqa: F405
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
