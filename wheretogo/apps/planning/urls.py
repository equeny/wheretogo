from django.conf.urls import patterns, url

from views import friends_choose, friends_analize

urlpatterns = patterns('',
    url(r'^choose/$', friends_choose, name='friends_choose'),
    url(r'^analize/$', friends_analize, name='friends_analize'),
)
