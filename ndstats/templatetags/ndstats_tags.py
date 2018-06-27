from django import template
from django.template import Template, Context
from ndstats.models import TEAM_EMP

register = template.Library()


@register.filter(name='lookup')
def cut(value, arg):
    try:
        return value[arg]
    except (IndexError, KeyError):
        return ''


@register.simple_tag
def player_line(player, team, is_comm=False):
    if not player:
        return Template("<td colspan='5'></td>").render(Context())
    if is_comm:
        ptime = player.time_empire_cmd if team == TEAM_EMP else player.time_consortium_cmd
    else:
        ptime = player.time_empire if team == TEAM_EMP else player.time_consortium

    if ptime:
        m, s = int(ptime / 60), ptime % 60
    else:
        m, s = 0, 0

    return Template('''<td class="text-left">
        <a href="{{ player.player.get_absolute_url }}">{{ player }}</a></td>
      <td>{{ player.score }}</td>
      <td>{{ player.kills }}</td>
      <td>{{ player.buildings }}</td>
      <td>{{ time_m }}:{{ time_s }}</td>
    ''').render(Context({
        'player': player,
        'time_m': m,
        'time_s': ('0%s' % s)[-2:],
    }))
