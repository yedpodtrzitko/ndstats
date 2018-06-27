import re
from ndstats.loggers import UnknownLineError
from ndstats.models import MatchEvent, TEAM_CHOICES_REVERSE

IGNORE_ACTIONS = (
    'resource_captured',
    'research_complete',
    'damaged_opposite_bunker',
)

# <627> <0> <-900.000000 5880.00
# <index> <type> <x y z>
re_structure = re.compile(
    '^<(\d+)> <([a-z_]+)> <(-?\d+.\d+) (-?\d+.\d+) (-?\d+.\d+)>')


def log(timestamp, line, re_match, active_match):
    team_name = re_match.group(1)
    action = re_match.group(2)
    if action == 'Round End':
        return True
    elif action == 'Destroyed Bunker':  # this doesnt trigger Round End
        active_match.set_winner(team_name)
        return True
    elif action == 'Eliminated Team':  # this doesnt trigger Round End
        active_match.set_winner(team_name)
        return True
    elif action == 'round_win':
        active_match.set_winner(team_name)
        return True
    elif action == 'round_lose':
        # active_match.set_loser(team_name)
        return True
    elif action == 'Surrendered':
        active_match.set_loser(team_name)
        return True
    elif action == 'structure_built':
        if team_name == '#ND_Team_Unassigned':
            return

        extra = str(re_match.group(3)).strip()
        re_s = re_structure.match(extra)
        MatchEvent.objects.get_or_create(
            entity=int(re_s.group(1)),
            match=active_match,
            defaults=dict(
                when=timestamp,
                what=MatchEvent.EVENT_BUILT,
                team=TEAM_CHOICES_REVERSE[team_name],
                where_x=float(re_s.group(3)),
                where_y=float(re_s.group(4)),
                where_z=float(re_s.group(5)),
                entype=re_s.group(2)
            )
        )
        return True

    if action in IGNORE_ACTIONS:
        return True

    raise UnknownLineError()
