import re

from ndstats.loggers import UnknownLineError

re_ignore_line = re.compile((
    '^('
    'Log file|'
    'Started map|'
    'rcon from|'
    '\[META\]|'
    'server|'
    'STEAMAUTH:|'
    '"Console<\d+>"|'
    '"(\w+)" = "(.*)"|'
    'Team ".*?" scored|'
    'Connection to Steam|'
    'Public IP|'
    'Assigned anonymous|'
    'VAC secure|'
    'HLX:CE|'
    'EmitSoundByHandle|'
    'cake_collected|'
    'Banid:|'
    'Server triggered "RESTART"'
    ')'
))


def log(timestamp, line, active_match):
    line = line.strip()
    if re_ignore_line.match(line):
        return True

    raise UnknownLineError()
