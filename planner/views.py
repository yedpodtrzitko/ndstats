# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import TemplateView, RedirectView, FormView
from planner.forms import MapForm
from planner.models import Event, Participant, STATUS_CHOICES, EventMap, \
    STATUS_STORY
from social.apps.django_app.default.models import UserSocialAuth


class PlannerView(TemplateView):
    template_name = 'planner.html'

    def get_context_data(self, **kwargs):
        data = super(PlannerView, self).get_context_data(**kwargs)
        data['events'] = Event.objects.filter(when__gte=now().date())
        data['states'] = STATUS_CHOICES
        data['stories'] = STATUS_STORY
        return data


class ChangeMapView(FormView):
    permanent = False
    template_name = '404.html'
    form_class = MapForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('planner')

    def form_valid(self, form):
        maps = form.cleaned_data.get('maps')
        participant, created = Participant.objects.get_or_create(
                event_id=self.kwargs['event'],
                player=UserSocialAuth.objects.get(user_id=self.request.user.pk),
        )
        participant.maps.clear()
        for map in maps[:participant.event.rounds]:
            EventMap.objects.create(
                event=participant.event,
                participant=participant,
                map=map)
        return super(ChangeMapView, self).form_valid(form)


class ChangeAttendView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return (reverse('planner'))

    def post(self, request, *args, **kwargs):
        states = dict(STATUS_CHOICES)

        state = request.POST.get('state', '')
        if state in states.keys():
            part, created = Participant.objects.get_or_create(
                event_id=kwargs['event'],
                player=UserSocialAuth.objects.get(user_id=request.user.pk),
                defaults={
                    'status': state,
                }
            )

            if not created:
                part.status = state
                part.save()

        return super(ChangeAttendView, self).post(request, *args, **kwargs)


class MotdView(TemplateView):
    template_name = 'motd.html'

    def get_context_data(self, **kwargs):
        data = super(MotdView, self).get_context_data(**kwargs)

        events = Event.objects.filter(when__gte=now.date())
        if events:
            data['event'] = events[0]
            data['players'] = Participant.objects.filter(event=data['event'],
                                                         status__in=(
                                                         'com', 'yes'))

        return data
