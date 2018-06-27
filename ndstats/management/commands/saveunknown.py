from django.core.management.base import BaseCommand
from ndstats.models import UnknownLine, Chatlog
from ndstats.parser import LogParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        parser = LogParser()

        Chatlog.objects.all().delete()

        for line in UnknownLine.objects.all():
            try:
                if '><BOT><' in line.line:
                    continue

                parser.parse_line(
                    line.ip_address, line.line,
                    save_unknown=False)
            except Exception as e:
                raise
            else:
                continue
                delete = raw_input('delete? (y/N)')
                # TODO - remove question
                if delete.strip().lower() == 'y':
                    line.delete()
