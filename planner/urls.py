from django.conf.urls import url, include
from django.contrib import admin
from planner.views import PlannerView, ChangeAttendView, MotdView, ChangeMapView

urlpatterns = [
    url('^change-attend/(?P<event>\d+)/$', ChangeAttendView.as_view(), name='change-attend'),
    url('^change-map/(?P<event>\d+)/$', ChangeMapView.as_view(), name='change-map'),
    url('^motd/$', MotdView.as_view(), name='motd'),
]
