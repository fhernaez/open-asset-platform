"""Event publication and dispatch (idempotent, in-process handlers)."""

from __future__ import annotations

import logging
from collections.abc import Callable

from django.db import transaction

from events.models import OutboxEvent

logger = logging.getLogger(__name__)

_handlers: dict[str, list[Callable]] = {}


def subscribe(event_type: str, handler: Callable) -> None:
    _handlers.setdefault(event_type, []).append(handler)


class EventPublisher:
    @staticmethod
    def publish(
        *,
        event_type: str,
        aggregate_type: str,
        aggregate_id: str,
        payload: dict | None = None,
        tenant_id=None,
        project_id=None,
        same_tx: bool = True,
    ) -> OutboxEvent:
        event = OutboxEvent(
            event_type=event_type,
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            payload=payload or {},
            tenant_id=tenant_id,
            project_id=project_id,
        )
        if same_tx:
            event.save()
            transaction.on_commit(lambda: EventPublisher._dispatch_async(event.pk))
        else:
            event.save()
            EventPublisher._dispatch_async(event.pk)
        return event

    @staticmethod
    def _dispatch_async(pk) -> None:
        # In-process dispatch after commit; external transport is a later concern.
        try:
            event = OutboxEvent.objects.get(pk=pk)
        except OutboxEvent.DoesNotExist:
            return
        for handler in _handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception:  # noqa: BLE001 - handler failure must not break commit
                logger.exception("Outbox handler failed for %s", event.event_type)


def dispatch_pending(batch_size: int = 200) -> int:
    """Dispatch pending events; used by the event-worker service."""
    from django.utils import timezone

    dispatched = 0
    qs = OutboxEvent.objects.filter(status=OutboxEvent.Status.PENDING).order_by("occurred_at")[:batch_size]
    for event in qs:
        failed = False
        for handler in _handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception:  # noqa: BLE001
                event.attempts += 1
                if event.attempts >= 5:
                    event.status = OutboxEvent.Status.FAILED
                event.save(update_fields=["attempts", "status"])
                failed = True
        if not failed:
            event.status = OutboxEvent.Status.PUBLISHED
            event.published_at = timezone.now()
            event.save(update_fields=["status", "published_at"])
            dispatched += 1
    return dispatched
