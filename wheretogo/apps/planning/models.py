import logging
import urllib
import urllib2

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from profiles.models import FacebookProfile


logger = logging.getLogger("mmp.%s" % __name__)


class PlaceManager(models.Manager):

    # def get_query_set(self):
    #     return PlaceQuerySet(self.model)

    # def __getattr__(self, attr, *args):
    #     try:
    #         return getattr(self.__class__, attr, * args)
    #     except AttributeError:
    #         return getattr(self.get_query_set(), attr, * args)

    def grab_places(lat, long, radius, oauth_token):
        '''fetch places from facebook from give circle'''

        #urllib2.
        print 'Hello'


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    fid = models.CharField(_('Facebook id'), max_length=50, unique=True)

    objects = PlaceManager()


class Planning(models.Model):
    organizer = models.ForeignKey(FacebookProfile, related_name='plannings')
    profiles = models.ManyToManyField(
        FacebookProfile, related_name='planning_involved_in'
    )
    lat = models.FloatField(_('Latitude'), default=50.435462778)
    lon = models.FloatField(_('Latitude'), default=30.48955857)
    # 50, 30 - should be Kiev coordinates
    radius = models.FloatField(_('Radius'), default=10000)

    def find_where_to_go(self):
        pass


class PlanningResultPlace(models.Model):
    planning = models.ForeignKey(Planning)
    place = models.ForeignKey(Place)
    rank = models.FloatField(default=0)
