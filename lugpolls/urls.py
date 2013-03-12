from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lugpolls.views.home', name='home'),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/profile/', 'lugpolls.views.profile', name='profile'),
)

# This serves up staticfiles at STATIC_URL when debug=True
urlpatterns += staticfiles_urlpatterns()
