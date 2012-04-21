from django.conf.urls import patterns, include, url
from django.contrib import admin


from core.views import home, logout

from profiles.models import new_users_handler
from social_auth.signals import socialauth_registered

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^logout/$', logout, name='logout'),
    url(r'', include('social_auth.urls')),
)

socialauth_registered.connect(new_users_handler, sender=None)
