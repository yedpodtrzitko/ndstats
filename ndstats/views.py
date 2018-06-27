from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.views.generic.detail import BaseDetailView
from ndstats.models import Chatlog, Match, Player, Server, MatchPlayer, TEAM_EMP, TEAM_CONS, FoodProduct
from django.views.decorators.cache import patch_cache_control
from functools import wraps


def never_ever_cache(decorated_function):
    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(
            response, no_cache=True, no_store=True, must_revalidate=True,
            max_age=0)
        return response

    return wrapper


class ChatView(ListView):
    paginate_by = 200
    model = Chatlog
    template_name = 'chatlogs_list.html'
    server = None

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        if 'pk' not in self.kwargs:
            first = Server.objects.filter(active=True).first()
            if not first:
                return redirect(reverse('players'))
            return redirect(reverse('chat', args=[first.pk]))

        self.server = get_object_or_404(Server, pk=self.kwargs['pk'])
        return super(ChatView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(match__server_id=self.server.pk)

    def get_context_data(self, **kwargs):
        data = super(ChatView, self).get_context_data(**kwargs)
        data['server'] = self.server
        data['servers'] = Server.objects.filter(active=True)
        return data


class MatchList(ListView):
    paginate_by = 50
    model = Match
    template_name = 'match_list.html'

    def get_queryset(self):
        return self.model.objects.filter(server__active=True,
                                         finished__isnull=False,
                                         started__isnull=False)


class PlayerList(ListView):
    paginate_by = 100
    template_name = 'player_list.html'
    model = Player
    ordering = ('-score',)

    def get_context_data(self, **kwargs):
        data = super(PlayerList, self).get_context_data(**kwargs)
        data['offset'] = 0
        return data


class PlayerDetail(DetailView):
    model = Player
    template_name = 'player_detail.html'


class MatchDetail(DetailView):
    model = Match
    template_name = 'match_detail.html'

    def get_context_data(self, **kwargs):
        data = super(MatchDetail, self).get_context_data(**kwargs)
        data['final_range'] = range(max(
            len(self.object.players[TEAM_EMP]),
            len(self.object.players[TEAM_CONS])) + 1)

        return data


class MatchLastRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        match = Match.objects.filter(server_id=self.kwargs['pk'],
                                     finished__isnull=False).order_by(
            '-finished').first()
        return reverse('match_last_detail', args=[match.pk])

    @never_ever_cache
    def get(self, request, *args, **kwargs):
        return super(MatchLastRedirect, self).get(request, *args, **kwargs)


class MatchLastDetail(MatchDetail):
    template_name = 'match_last_detail.html'


class ServerList(DetailView):
    model = Server
    template_name = 'server_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if 'pk' not in self.kwargs:
            first = Server.objects.filter(active=True).first()
            if not first:
                return redirect(reverse('players'))
            return redirect(reverse('servers', args=[first.pk]))

        try:
            self.server = Server.objects.get(pk=self.kwargs['pk'])
        except Server.DoesNotExist:
            raise Http404('server not found')

        return super(ServerList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(ServerList, self).get_context_data(**kwargs)
        data['servers'] = Server.objects.filter(active=True)
        return data


class WeeklyStatsView(TemplateView):
    model = Server
    template_name = 'stats_weekly.html'

    def get_context_data(self, **kwargs):
        week_ago = datetime.now() - timedelta(days=7)
        matches = Match.objects.filter(started__gte=week_ago)

        match_players = MatchPlayer.objects. \
                            filter(match__in=matches). \
                            select_related(). \
                            values('player', 'player__nick'). \
                            annotate(Sum('kills'), player_score=Sum('score')). \
                            order_by('-player_score')[:20]

        data = super(WeeklyStatsView, self).get_context_data(**kwargs)
        data['match_players'] = match_players
        return data


class MatchEventsJson(BaseDetailView):
    model = Match

    def render_to_response(self, context):
        events = self.get_object().matchevent_set.distinct('entity').order_by(
            'entity')
        dumped = []
        for e in events:
            if not (e.where_x and e.where_y):
                continue

            x = {
                'when': e.when.isoformat(),
                'what': e.what,
                'team': e.team,
                'x': e.where_x,
                'y': e.where_y,
                'id': e.entity,
                'entype': e.entype,
            }
            dumped.append(x)

        return JsonResponse(data=dumped, safe=False)


class FoodProductsList(ListView):
    model = FoodProduct
    template_name = 'fp_list.html'


class FoodProductDetail(DetailView):
    model = FoodProduct
    template_name = 'fp_detail.html'
