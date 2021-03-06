from django.conf.urls import patterns, url

from views import friends_choose, friends_analize, planning_list, planning_status, \
planning_results, place_rate

urlpatterns = patterns('',
    url(r'^friends/choose/$', friends_choose, name='friends_choose'),
    url(r'^friends/analize/$', friends_analize, name='friends_analize'),
    url(r'^$', planning_list, name='planning_plannings'),
    url(r'^(?P<id>[\d]+)/status/$', planning_status, name='planning_status'),
    url(r'^(?P<id>[\d]+)/results/$', planning_results, name='planning_results'),
    url(r'^(?P<plan_id>\d+)/(?P<place_id>\d+)/mark/$', place_rate, name='place_rate'),
)
