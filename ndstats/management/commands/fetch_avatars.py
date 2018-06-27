from time import sleep

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Sum, Max, F
from ndstats.models import MatchPlayer, Match, Player
from valve.steam.id import SteamID

FETCH_URL = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'

res = {
    'response': {
        'players': [
            {
                'steamid': '76561198039900308',
                'profilestate': 1,
                'primaryclanid': '103582791437067880',
                'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/54/54be38c13d0e7792de2af9a76c4e376766cf697a_full.jpg',
                'timecreated': 1301204719,
                'communityvisibilitystate': 3,
                'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/54/54be38c13d0e7792de2af9a76c4e376766cf697a.jpg',
                'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/54/54be38c13d0e7792de2af9a76c4e376766cf697a_medium.jpg',
                'lastlogoff': 1468175511,
                'personastateflags': 0,
                'profileurl': 'http://steamcommunity.com/profiles/76561198039900308/',
                'personastate': 3,
                'personaname': 'Mallurnstarsong',
            },
        ]
    }
}


# ?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids=123,345&format=json


class Command(BaseCommand):
    def handle(self, *args, **options):
        players = Player.objects.filter(avatar__isnull=True).order_by('-score')
        i = 0
        ids = {}

        for player in players:
            ids[str(SteamID.from_text(player.id).as_64())] = player
            i += 1
            if i >= 99:
                response = requests.get(
                    FETCH_URL, params={
                        'key': settings.STEAM_KEY,
                        'steamids': ','.join(ids.keys()),
                        'format': 'json',
                    },
                    headers={
                        'referer': 'http://ndix.vanyli.net',
                    },
                )
                i = 0

                if response.ok:
                    print('fetched data')

                    for pdata in response.json()['response']['players']:
                        ids[pdata['steamid']].avatar = pdata['avatar']
                        ids[pdata['steamid']].nick = pdata['personaname']
                        ids[pdata['steamid']].save()

                    sleep(5)
