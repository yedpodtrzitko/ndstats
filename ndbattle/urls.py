from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    # url(r'^events/', include('planner.urls')),
    url(r'^logout/$', logout, kwargs={'next_page': '/'}, name='logout'),
    url(r'^', include('ndstats.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

