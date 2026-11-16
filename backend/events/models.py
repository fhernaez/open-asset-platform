"""Transactional outbox: domain events persisted atomically with business data."""

from __future__ import annotations

import uuid

from django.db import models

from core.models import UUIDPkModel


class OutboxEvent(UUIDPkModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        PUBLISHED = "published"
        FAILED = "failed"

    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    event_type = models.CharField(max_length=160, db_index=True)
    aggregate_type = models.CharField(max_length=80)
    aggregate_id = models.CharField(max_length=80)
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    project_id = models.UUIDField(null=True, blank=True, db_index=True)
    payload = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True, db_index=True)
    available_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)

    class Meta:
        db_table = "events_outboxevent"
        ordering = ["occurred_at"]
        indexes = [models.Index(fields=["status", "occurred_at"])]

    def __str__(self) -> str:
        return f"{self.event_type}:{self.aggregate_id}"
