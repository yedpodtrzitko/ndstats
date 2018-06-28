import json

from django.conf import settings
import re

from ndstats.models import Player, MatchPlayer, Server, UnknownLine
from ndstats.loggers import UnknownLineError

from datetime import datetime

from .loggers import player as log_player
from .loggers import generic as log_generic
from .loggers import team as log_team
from .loggers import world as log_match


class LogParser(object):
    # format of: (IP):(port)|(unicode noise)L(actual data)
    re_is_log = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\|.?L (.*)', re.UNICODE)
    # yed_<2><STEAM_1:0:33657626><CONSORTIUM>
    re_actor = re.compile(r'^"(.*?)<(\d+)><(STEAM_.*?)><(.*?)>" (.*)$')

    # (victim_position "688 1133 -4")
    re_victim_position = re.compile(r'(?:.*)victim_position \"(-?\d+) (-?\d+) (-?\d+)\"\)')

    # World triggered "Round_Start"
    # World triggered "Round_Win"
    # World triggered "map_changed" <hydro>
    re_world = re.compile(r'^World triggered "(.*?)"(.*)')

    # Team "CONSORTIUM" triggered "round_win"
    # Team "EMPIRE" triggered "round_lose"
    re_team = re.compile(r'^Team "(.*?)" triggered "(.*?)"(.*)')

    _servers = {}

    def __init__(self):
        self._active_match = {}
        self._servers = {(s.ip, s.port): s for s in Server.objects.all()}

    def get_server(self, ip_address, port):
        if (ip_address, port) in self._servers:
            return self._servers[ip_address, port]

        server = Server.objects.create(ip=ip_address, port=port)
        self._servers[ip_address, port] = server

        return self._servers[ip_address, port]

    def parse_raw_line(self, raw_json):
        """
        entry point for saving log
        """

        json_line = json.loads(raw_json.decode('utf-8'))
        line = json_line['Payload']
        is_rl = self.re_is_log.match(line)
        if not is_rl:
            return

        ip = is_rl.group(1)
        port = is_rl.group(2)
        line = is_rl.group(3)

        try:
            self.parse_line(ip, int(port), line.strip())
        except UnknownLineError:
            UnknownLine.objects.create(
                ip_address=ip,
                line=line
            )
        else:
            if getattr(settings, 'DEBUG_UNKNOWN', False):
                UnknownLine.objects.create(
                    ip_address=ip,
                    line=line
                )

    def parse_line(self, ip_address, port, raw_line, save_unknown=True):
        # cut off datetime
        line = raw_line[23:]

        # get datetime
        line_dt = raw_line[:21]
        timestamp = datetime.strptime(line_dt, "%m/%d/%Y - %H:%M:%S")

        server = self.get_server(ip_address, port)

        if line.startswith('Loading map'):
            server.finish_all(timestamp)
            return True

        re_world = self.re_world.match(line)
        if re_world:
            self._active_match[ip_address, port] = log_match.log(timestamp, line, re_world, server)
            return True

        if not self._active_match.get(ip_address, port):
            self._active_match[ip_address, port] = server.get_unfinished().first()

        if not self._active_match.get(ip_address, port):
            return True

        re_team = self.re_team.match(line.strip())
        if re_team:
            return log_team.log(timestamp, line, re_team, self._active_match[ip_address, port])

        # is it about player?
        re_player = self.re_actor.match(line)
        if re_player:
            player_name = re_player.group(1)
            # client_id = re_player.group(2)
            player_id = re_player.group(3)
            player_team = re_player.group(4)
            strip_line = re_player.group(5)
            match_player = self.parse_player(player_id, player_name,
                                             self._active_match[ip_address, port])
            return log_player.log(timestamp, strip_line, match_player, player_team, self)

        # it's about some generic stuff
        return log_generic.log(timestamp, line, self._active_match[ip_address, port])

    def parse_player(self, player_id, player_nick, match):
        """
        (u'djfishfish', u'37', u'STEAM_1:0:29258395', u'CONSORTIUM',)
        """
        # TODO - cache
        player = Player.objects.get_or_create(
            id=player_id,
            defaults=dict(nick=player_nick)
        )[0]

        return MatchPlayer.objects.get_or_create(
            match=match,
            player=player,
        )[0]
