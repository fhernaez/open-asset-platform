#!/usr/bin/env python
"""Idempotent DB bootstrap (db-bootstrap one-shot service).

Creates the application role and database if they are missing, then installs the
required extensions (postgis) and schemas. Safe to run on a fresh
volume or on a pre-existing cluster that lacks the OAP database. It never drops
or alters existing databases/roles and uses an advisory lock to serialize
concurrent runs. Exits non-zero if a required extension cannot be installed.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import psycopg
from psycopg import sql

IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

LOCK_KEY = 0x4F41505F424F4F54  # "OAP_BOOT"


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def _read_secret(name: str, file_var: str) -> str:
    path = os.environ.get(file_var, "")
    if path and Path(path).exists():
        return Path(path).read_text(encoding="utf-8").strip()
    return os.environ.get(name, "")


def _validate_identifier(value: str, label: str) -> None:
    if not IDENTIFIER_RE.match(value):
        raise SystemExit(f"[db-bootstrap] invalid {label}: {value!r}")


def _wait_for_db(host: str, port: int, admin_user: str, admin_password: str, timeout: int = 120) -> psycopg.Connection:
    deadline = time.time() + timeout
    last_exc: Exception | None = None
    while time.time() < deadline:
        try:
            conn = psycopg.connect(
                host=host,
                port=port,
                dbname="postgres",
                user=admin_user,
                password=admin_password,
                connect_timeout=5,
            )
            conn.autocommit = True
            return conn
        except psycopg.Error as exc:  # noqa: PERF203
            last_exc = exc
            time.sleep(2)
    raise SystemExit(f"[db-bootstrap] database not reachable: {last_exc}")


def _create_role(conn: psycopg.Connection, role: str, password: str) -> bool:
    cur = conn.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (role,))
    if cur.fetchone():
        return False
    conn.execute(sql.SQL("CREATE ROLE {} LOGIN").format(sql.Identifier(role)))
    conn.execute(sql.SQL("ALTER ROLE {} WITH PASSWORD %s").format(sql.Identifier(role)), (password,))
    return True


def _create_database(conn: psycopg.Connection, dbname: str, owner: str) -> bool:
    cur = conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
    if cur.fetchone():
        return False
    conn.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(sql.Identifier(dbname), sql.Identifier(owner)))
    return True


def _install_extensions(
    host: str, port: int, dbname: str, app_user: str, app_password: str, extensions: list[str]
) -> None:
    conn = psycopg.connect(host=host, port=port, dbname=dbname, user=app_user, password=app_password)
    conn.autocommit = True
    try:
        for ext in extensions:
            if not IDENTIFIER_RE.match(ext):
                raise SystemExit(f"[db-bootstrap] invalid extension name: {ext!r}")
            try:
                conn.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS {}").format(sql.Identifier(ext)))
            except psycopg.Error as exc:
                raise SystemExit(f"[db-bootstrap] failed to install extension {ext!r}: {exc}") from exc
        for schema in ("core", "telemetry", "plugins"):
            if IDENTIFIER_RE.match(schema):
                conn.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema)))
    finally:
        conn.close()


def main() -> int:
    host = _env("DB_HOST", "db")
    port = int(_env("DB_PORT", "5432"))
    admin_user = _env("DB_ADMIN_USER", "postgres")
    admin_password = _read_secret("DB_ADMIN_PASSWORD", "DB_ADMIN_PASSWORD_FILE")
    dbname = _env("DB_NAME", "oap")
    app_user = _env("DB_APP_USER", "oap_app")
    app_password = _read_secret("DB_APP_PASSWORD", "DB_APP_PASSWORD_FILE")
    extensions = [e.strip() for e in _env("DB_REQUIRED_EXTENSIONS", "postgis").split(",") if e.strip()]

    for value, label in ((dbname, "DB_NAME"), (app_user, "DB_APP_USER")):
        _validate_identifier(value, label)

    if not admin_password:
        raise SystemExit("[db-bootstrap] DB_ADMIN_PASSWORD(_FILE) is required")
    if not app_password:
        raise SystemExit("[db-bootstrap] DB_APP_PASSWORD(_FILE) is required")

    conn = _wait_for_db(host, port, admin_user, admin_password)

    role_created = False
    db_created = False
    try:
        conn.execute("SELECT pg_advisory_lock(%s)", (LOCK_KEY,))
        role_created = _create_role(conn, app_user, app_password)
        db_created = _create_database(conn, dbname, app_user)
        conn.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
    except BaseException:
        conn.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
        raise
    finally:
        conn.close()

    _install_extensions(host, port, dbname, app_user, app_password, extensions)

    print(
        f"[db-bootstrap] OK role_created={role_created} db_created={db_created} "
        f"extensions={','.join(extensions)} db={dbname} user={app_user}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
