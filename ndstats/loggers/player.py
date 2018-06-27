import re

from ndstats.models import Chatlog, MatchEvent, TEAM_CHOICES_REVERSE
from ndstats import loggers


IGNORE_LINES = (
    'STEAM USERID validated',
    'entered the game',
)

IGNORE_ACTIONS = (
    'STEAMAUTH:',
)

re_triggered = re.compile(r'^triggered "(.*?)"(.*)')
re_joined = re.compile(r'^joined team "(.*)"$')


def log(timestamp, line, match_player, player_team, log_parser):
    if line in IGNORE_LINES:
        return True

    action = line.split(' ')[0]

    if action in ('say', 'say_team', 'say_squad'):
        private = action != 'say'
        team = match_player.team_current
        return chat(match_player, timestamp, line[len(action)+2:-1], team, private)
    elif action == 'disconnected':
        return match_player.disconnect(timestamp)
    elif action == 'connected,':
        ip = line[len('connected, address "'):-1]
        if ':' in ip:
            ip = ip.split(':')[0]
        match_player.player.save_ip(timestamp, ip)
        return True
    elif action == 'triggered':
        re_matched = re_triggered.match(line)
        action_trigger = re_matched.group(1)
        if action_trigger.endswith('_destroyed') or action_trigger == 'structure_kill':
            return match_player.kill_structure()
        elif action_trigger == 'clantag':
            line = line[:-2]
            clantag = line[line.rfind('"') + 1:]
            return match_player.player.set_clantag(clantag)
        elif action_trigger == 'promoted_to_commander':
            return match_player.promote_to_commander(timestamp)
        elif action_trigger in ('killed_commander', 'headshot'):
            return True
        elif action_trigger in ('weaponstats', 'weaponstats2'):
            match_player.change_team(timestamp, player_team)
            return True
        elif action_trigger == 'weaponstats3':
            #"yed_<2><STEAM_1:0:33657626><EMPIRE>" triggered "weaponstats3" (score "-15")
            score = re_matched.group(2)[9:-2]
            match_player.update_score(score)
            return True
    elif action == 'joined':
        re_team = re_joined.match(line).group(1)
        match_player.change_team(timestamp, re_team)
        return True
    elif action == 'changed':
        if line.startswith('changed role to'):
            match_player.change_team(timestamp, player_team)
            return True
        if line.startswith('changed name to'):
            return match_player.player.set_nick(line[17:-1])
    elif action == 'committed':
        return match_player.suicide()
    elif action == 'killed':
        line = line[len(action)+1:].lstrip()
        re_whom = log_parser.re_actor.match(line)
        if re_whom:
            victim_nick = re_whom.group(1)
            victim_id = re_whom.group(3)
            victim_team = re_whom.group(4)
            victim = log_parser.parse_player(victim_id, victim_nick,
                                             match_player.match)
            victim.died()
            re_pos = log_parser.re_victim_position.match(line)
            if re_pos:
                MatchEvent.objects.create(
                    match=victim.match,
                    what=MatchEvent.EVENT_DEATH,
                    when=timestamp,
                    team=TEAM_CHOICES_REVERSE[victim_team],
                    where_x=re_pos.group(1),
                    where_y=re_pos.group(2),
                    where_z=re_pos.group(3),
                )

        return match_player.kill()

    raise loggers.UnknownLineError()


def chat(match_player, timestamp, line, team, private):
    line = line.strip()
    if not line:
        return True

    return Chatlog.objects.create(
        match_id=match_player.match_id,
        player_id=match_player.player_id,
        message=line,
        timestamp=timestamp,
        private=private,
        team=team
    )
