from django.core.management.base import BaseCommand
from django.db.models import Sum, Max, F
from ndstats.models import MatchPlayer, Match, Player


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''
        delete from ndstats_matchplayer where match_id in (select match_id from ndstats_matchplayer group by match_id having count(player_id) < 4 );

        // not needed
        delete from ndstats_match where id in (select match_id from ndstats_matchplayer group by match_id having count(player_id) < 4 );



        update ndstats_chatlog set match_id = 233 where match_id not in (select distinct match_id from ndstats_matchplayer);

        delete from ndstats_matchevent where match_id not in (select distinct match_id from ndstats_matchplayer);
        delete from ndstats_match where finished is not null and id not in (select distinct match_id from ndstats_matchplayer);
        '''
