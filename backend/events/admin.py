from django.contrib import admin

from events.models import OutboxEvent


@admin.register(OutboxEvent)
class OutboxEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "aggregate_type", "aggregate_id", "status", "attempts", "occurred_at"]
    list_filter = ["status", "event_type"]
