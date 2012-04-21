import logging
import urllib
import urllib2
import json

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from profiles.models import FacebookProfile


logger = logging.getLogger("wheretogo.%s" % __name__)


# TODO: move to settings.py
VALID_PLACE_CATEGORIES = [
    #'Airport',
    'Arts/Entertainment/Nightlife',
    'Attractions/Things to Do',
    'Automotive',
    'Bank/Financial Services',
    'Bar',
    'Book Store',
    'Business Services',
    'Church/Religious Organization',
    'Club',
    'Community/Government',
    'Concert Venue',
    'Education',
    'Event Planning/Event Services',
    'Food/Grocery',
    'Health/Medical/Pharmacy',
    'Home Improvement',
    'Hospital/Clinic',
    'Hotel',
    'Landmark',
    'Library',
    #'Local Business',
    'Movie Theater',
    'Museum/Art Gallery',
    'Outdoor Gear/Sporting Goods',
    'Pet Services',
    'Professional Services',
    'Public Places',
    'Real Estate',
    'Restaurant/Cafe',
    'School',
    'Shopping/Retail',
    'Spas/Beauty/Personal Care',
    'Sports Venue',
    'Sports/Recreation/Activities',
    'Tours/Sightseeing',
    'Transit Stop',
    'Transportation',
    #'University',
]


class PlaceManager(models.Manager):

    # def get_query_set(self):
    #     return PlaceQuerySet(self.model)

    # def __getattr__(self, attr, *args):
    #     try:
    #         return getattr(self.__class__, attr, * args)
    #     except AttributeError:
    #         return getattr(self.get_query_set(), attr, * args)

    def grab_places(self, lat, lon, radius, oauth_token):
        '''fetch places from facebook from give circle'''

        path = 'https://graph.facebook.com/search?%s' % urllib.urlencode({
            'type': 'place',
            'center': "%f,%f" % (lat, lon),
            'distance': "%.0f" % radius,
            'access_token': oauth_token,
            'limit': 1000
        })
        response = urllib2.urlopen(path)
        data = json.loads(response.read())
        # TODO retrieve info from next pages if numbers less than 500
        for place in data['data']:
            logger.debug('Adding place "%s" to db' % place['name'])
            if place['category'] not in VALID_PLACE_CATEGORIES:
                continue

            Place.objects.get_or_create(
                name=place['name'],
                fid=place['id'],
                category=place['category'],
                lat=place['location']['latitude'],
                lon=place['location']['longitude']
            )


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    fid = models.CharField(_('Facebook id'), max_length=50, unique=True)
    lat = models.FloatField(_('Latitude'))
    lon = models.FloatField(_('Latitude'))
    category = models.CharField(_('Category'), max_length=50)

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

    def find_where_to_go(self, oauth_token):
        # getting places in current radius
        Place.grab_places(self.lat, self.log, self.radius, oauth_token)

        # getting facebook profiles checkins
        for profile in [self.organizer] + self.profiles.all():
            path = 'https://graph.facebook.com/%s/checkins' % profile.fid
            response = urllib2.urlopen(path)
            data = json.loads(response.read())
            import ipdb
            ipdb.set_trace()



class PlanningResultPlace(models.Model):
    planning = models.ForeignKey(Planning)
    place = models.ForeignKey(Place)
    rank = models.FloatField(default=0)
