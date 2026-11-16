from django.core.management.base import BaseCommand

from events.services import dispatch_pending


class Command(BaseCommand):
    help = "Dispatch pending outbox events (idempotent)."

    def handle(self, *args, **options):
        dispatched = dispatch_pending()
        self.stdout.write(self.style.SUCCESS(f"dispatched={dispatched}"))
