from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import home, logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^logout/$', logout, name='logout'),
    url(r'', include('social_auth.urls')),
)
