from django.conf.urls import patterns, url

from views import friends_choose, friends_analize, planning_list

urlpatterns = patterns('',
    url(r'^friends/choose/$', friends_choose, name='friends_choose'),
    url(r'^friends/analize/$', friends_analize, name='friends_analize'),
    url(r'^$', planning_list, name='planning_plannings'),
)
