from django.core.management.base import BaseCommand
from django.db.models import Sum, Max, F
from ndstats.models import MatchPlayer, Match, Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            saved_until = Player.objects.annotate(Max('score_saved')).first().score_saved__max
        except AttributeError:
            saved_until = 0

        qs = MatchPlayer.objects.select_related('player').filter(
            match_id__gt=saved_until).values('player_id').annotate(
            Sum('score')).order_by('-score__sum')

        try:
            last_match = Match.objects.latest('id').id
        except Match.DoesNotExist:
            last_match = 0

        for x in qs:
            Player.objects.filter(id=x['player_id']).update(
                score=F('score') + x['score__sum'], score_saved=last_match)
