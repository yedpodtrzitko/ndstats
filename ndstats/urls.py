from django.conf.urls import url
from django.views.generic import RedirectView
from ndstats.views import ChatView, MatchList, PlayerList, MatchDetail, \
    MatchLastDetail, MatchLastRedirect, ServerList, WeeklyStatsView, \
    PlayerDetail, MatchEventsJson

urlpatterns = [
    url(r'^servers/(?P<pk>\d+)/$', ServerList.as_view(), name='servers'),
    url(r'^servers/$', ServerList.as_view(), name='servers'),
    url(r'^players/$', PlayerList.as_view(), name='players'),
    url(r'^players/detail/(?P<pk>STEAM_1:[01]:\d+)/$', PlayerDetail.as_view(), name='player_detail'),
    url(r'^matches/$', MatchList.as_view(), name='match_list'),
    url(r'^matches/(?P<pk>\d+)/$', MatchDetail.as_view(), name='match_detail'),
    url(r'^matches/(?P<pk>\d+)/events/$', MatchEventsJson.as_view(), name='match_events'),
    url(r'^matches/last/(?P<pk>\d+)/$', MatchLastRedirect.as_view(), name='match_last_redirect'),
    url(r'^matches/motd/(?P<pk>\d+)/$', MatchLastDetail.as_view(), name='match_last_detail'),
    url(r'^matches/sum/$', WeeklyStatsView.as_view(), name='stats_week'),
    url(r'^chat/(?P<pk>\d+)/$', ChatView.as_view(), name='chat'),
    url(r'^chat/$', ChatView.as_view(), name='chat'),
    url(r'^$', RedirectView.as_view(url='matches', permanent=True), name='index'),
]
