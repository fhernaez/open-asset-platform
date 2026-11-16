"""Unit tests for the idempotent DB bootstrap orchestration (SQL execution mocked).

The real PostgreSQL/TimescaleDB run is covered by the Docker integration gate
(scripts/gates/G1.sh), which cannot execute in this sandbox (Docker daemon
lacks unshare/mount privileges). These tests verify the bootstrap control flow.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def bootstrap_module(monkeypatch, tmp_path):
    from scripts import ensure_db

    admin_pw = tmp_path / "admin_pw"
    app_pw = tmp_path / "app_pw"
    admin_pw.write_text("admin-secret")
    app_pw.write_text("app-secret")

    monkeypatch.setenv("DB_ADMIN_PASSWORD_FILE", str(admin_pw))
    monkeypatch.setenv("DB_APP_PASSWORD_FILE", str(app_pw))
    monkeypatch.setenv("DB_NAME", "oap")
    monkeypatch.setenv("DB_APP_USER", "oap_app")
    monkeypatch.setenv("DB_REQUIRED_EXTENSIONS", "postgis,timescaledb")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")

    calls = {"role": 0, "db": 0, "extensions": [], "lock": 0, "unlock": 0}

    class FakeConn:
        autocommit = True

        def execute(self, query, params=None):
            text = str(query)
            if "pg_advisory_lock" in text:
                calls["lock"] += 1
            elif "pg_advisory_unlock" in text:
                calls["unlock"] += 1
            return self

        def close(self):
            pass

    monkeypatch.setattr(ensure_db, "_wait_for_db", lambda *a, **k: FakeConn())

    def fake_create_role(conn, role, password):
        calls["role"] += 1
        return True  # first run creates

    def fake_create_database(conn, dbname, owner):
        calls["db"] += 1
        return True

    def fake_install_extensions(host, port, dbname, app_user, app_password, extensions):
        calls["extensions"] = extensions

    monkeypatch.setattr(ensure_db, "_create_role", fake_create_role)
    monkeypatch.setattr(ensure_db, "_create_database", fake_create_database)
    monkeypatch.setattr(ensure_db, "_install_extensions", fake_install_extensions)

    return ensure_db, calls


def test_bootstrap_creates_role_db_extensions(bootstrap_module):
    ensure_db, calls = bootstrap_module
    rc = ensure_db.main()
    assert rc == 0
    assert calls["role"] == 1
    assert calls["db"] == 1
    assert calls["extensions"] == ["postgis", "timescaledb"]
    assert calls["lock"] == 1
    assert calls["unlock"] == 1


def test_invalid_identifier_rejected(bootstrap_module, monkeypatch):
    ensure_db, _ = bootstrap_module
    monkeypatch.setenv("DB_NAME", "oap; drop database")
    with pytest.raises(SystemExit):
        ensure_db.main()


def test_missing_admin_password_rejected(bootstrap_module, monkeypatch, tmp_path):
    ensure_db, _ = bootstrap_module
    monkeypatch.setenv("DB_ADMIN_PASSWORD_FILE", str(tmp_path / "nonexistent"))
    with pytest.raises(SystemExit):
        ensure_db.main()


def test_identifier_regex():
    from scripts.ensure_db import IDENTIFIER_RE

    assert IDENTIFIER_RE.match("oap_app")
    assert not IDENTIFIER_RE.match("oap-app")
    assert not IDENTIFIER_RE.match("oap;drop")
