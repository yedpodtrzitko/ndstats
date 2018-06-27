from django.core.management.base import BaseCommand

from ndstats.utils import handle_log


class Command(BaseCommand):
    def handle(self, *args, **options):
        handle_log()
