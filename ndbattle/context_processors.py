from ndstats.models import TEAM_CONS, TEAM_EMP

VARIABLES = {
    'TEAM_CONS': TEAM_CONS,
    'TEAM_EMP': TEAM_EMP,
}


def settings_variables(request):
    return VARIABLES
