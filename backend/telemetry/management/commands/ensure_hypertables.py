"""Convert telemetry tables to TimescaleDB hypertables when available.

This is idempotent and a no-op on databases without the timescaledb extension
(never a silent fallback in production: the DB bootstrap job fails fast if the
extension is missing and the API does not start).
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import connection

HYPERTABLES = [
    ("telemetry_telemetrypoint", "ts"),
]


class Command(BaseCommand):
    help = "Ensure TimescaleDB hypertables exist (idempotent)."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("SELECT extname FROM pg_extension WHERE extname='timescaledb'")
            has_timescale = cursor.rowcount > 0
        if not has_timescale:
            self.stdout.write("timescaledb extension not present; skipping hypertables.")
            return
        created = 0
        with connection.cursor() as cursor:
            for table, time_column in HYPERTABLES:
                cursor.execute(
                    "SELECT create_hypertable(%s, %s, if_not_exists => TRUE)",
                    [table, time_column],
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"hypertables_checked={created}"))
