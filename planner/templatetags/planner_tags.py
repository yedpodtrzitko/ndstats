from django import template
from django.core.cache import cache

from planner.forms import MapForm
from planner.models import Participant

from social.apps.django_app.default.models import UserSocialAuth

register = template.Library()


@register.assignment_tag
def participate(event, user):
    socka = UserSocialAuth.objects.get(user=user)
    part, c = Participant.objects.get_or_create(event=event, player=socka)
    return part


@register.assignment_tag
def get_event_maps(event, user):
    try:
        part = Participant.objects.get(event=event, player=user)
    except Participant.DoesNotExist:
        maps_data = []
    else:
        maps_data = part.maps.all().values_list('pk', flat=True)

    return MapForm(data={'maps': maps_data})


@register.assignment_tag
def get_attend_count(user):
    res = cache.get('attend-count-%s' % user.pk)
    if res is None:
        res = Participant.objects.filter(player=user,
                                         status__in=['yes', 'com']).count()
        cache.set('attend-count-%s' % user.pk, res)
    return res
