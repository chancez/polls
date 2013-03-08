from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^accounts/profile/', 'user.views.profile', name='auth_profile'),
)

# This serves up staticfiles at STATIC_URL when debug=True
urlpatterns += staticfiles_urlpatterns()
