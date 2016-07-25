from django.contrib import admin
from django.conf.urls import include, url

from example.views import HomeView
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edc-visit-schedule/', include('edc_visit_schedule.urls')),
    url(r'^edc/', include('edc_base.urls')),
    url(r'^admin/$', RedirectView.as_view(pattern_name='home_url')),
    url(r'^', HomeView.as_view(), name='home_url'),
]
