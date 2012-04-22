# coding: utf-8

from datetime import datetime, timedelta
import time
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
    'arts/entertainment/nightlife',
    'attractions/things to do',
    #'automotive',
    #'bank/financial services',
    'bar',
    #'book store',
    #'business services',
    'church/religious organization',
    'club',
    #'community/government',
    'concert venue',
    #'education',
    #'event planning/event services',
    'food/grocery',
    #'health/medical/pharmacy',
    #'home improvement',
    #'hospital/clinic',
    #'hotel',
    'landmark',
    'library',
    #'local business',
    'movie theater',
    'museum/art gallery',
    'outdoor gear/sporting goods',
    #'pet services',
    #'professional services',
    'public places',
    #'real estate',
    'restaurant/cafe',
    #'school',
    'shopping/retail',
    'spas/beauty/personal care',
    'sports venue',
    'sports/recreation/activities',
    'tours/sightseeing',
    #'transit stop',
    #'transportation',
    #'university',
]


def normalize_place_category(cat_name, name):
    '''Many places have Local Business category, so we try to get more detailed category'''

    cat_name = cat_name.lower()
    words = name.lower().strip().split(' ')
    if cat_name == 'local business':
        if 'cafe' in words or 'restaurant' in words or 'café' in words \
        or 'sushi' in words or 'pizza' in words:
            return 'restaurant/cafe'
        elif 'cinema' in words:
            return 'movie theater'
        elif 'club' in words:
            return 'club'
        elif 'pub' in words or 'bar' in words:
            return 'bar'
    return cat_name


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
            'limit': 500
        })
        logger.debug('Trying to get places list from Facebook with url: %s' % path)
        response = urllib2.urlopen(path)
        data = json.loads(response.read())
        # TODO retrieve info from next pages if numbers less than 500
        results = []
        for place in data['data']:
            logger.debug('Trying to add place "%s" to db' % place['name'])
            place_category = normalize_place_category(place['category'], place['name'])
            if place_category not in VALID_PLACE_CATEGORIES:
                logger.debug(
                    'Place category is not valid(%s). Ignoring' % place_category
                )
                continue
            try:
                place_obj = Place.objects.get(
                    fid=place['id'],
                )
            except Place.DoesNotExist:
                place_obj = Place(fid=place['id'])
            if place_obj.likes_count < 0:
                # getting extended info about page from FB
                path = 'https://graph.facebook.com/%s' % place['id']
                response = urllib2.urlopen(path)
                page_data = json.loads(response.read())
                if not page_data:
                    logger.debug('Empty results for page %s' % place['id'])
                    continue
                place_obj.likes_count = page_data.get('likes', 0)

            place_obj.name = place['name']
            place_obj.fid = place['id']
            place_obj.category = place_category
            place_obj.lat = place['location']['latitude']
            place_obj.lon = place['location']['longitude']
            place_obj.save()
            results.append(place_obj)
        return results


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    fid = models.CharField(_('Facebook id'), max_length=50, unique=True)
    lat = models.FloatField(_('Latitude'))
    lon = models.FloatField(_('Latitude'))
    category = models.CharField(_('Category'), max_length=50)
    likes_count = models.PositiveIntegerField(default=-1)

    objects = PlaceManager()

    def __unicode__(self):
        return self.name


class Planning(models.Model):
    organizer = models.ForeignKey(FacebookProfile, related_name='plannings')
    profiles = models.ManyToManyField(
        FacebookProfile, related_name='planning_involved_in'
    )
    lat = models.FloatField(_('Latitude'), default=50.435462778)
    lon = models.FloatField(_('Latitude'), default=30.48955857)
    # 50, 30 - should be Kiev coordinates
    radius = models.FloatField(_('Radius'), default=10000)
    percent = models.FloatField(_('Percent completed'), default=0)

    STATUS_IN_PROGRESS = 1
    STATUS_DONE = 2
    STATUSES = (
        (STATUS_IN_PROGRESS, _('In progress')),
        (STATUS_DONE, _('Done'))
    )
    status = models.IntegerField(choices=STATUSES, default=STATUS_IN_PROGRESS)
    created = models.DateTimeField(auto_now_add=True)

    def find_where_to_go(self):

        # getting places in current radius
        self.status_events.create(
            message=_('Fetching  places from selected circle')
        )
        places = Place.objects.grab_places(
            self.lat, self.lon, self.radius, self.organizer.oauth_token
        )
        self.percent = 30
        self.save()
        # for faster check if user has checked in in current place
        place_ids = set([p.id for p in places])

        # getting facebook profiles checkins
        profiles = self.profiles.all()
        for i, profile in enumerate(profiles):
            self.status_events.create(
                message=_('Fetching  data for user %s...' % profile.name)
            )
            self.percent = 30 + i / len(profiles) * 50
            self.save()
            if profile.last_changes:
                # fetch only changes from last update
                path = 'https://graph.facebook.com/%s/locations?access_token=%s&since=%s' % (
                    profile.fid, self.organizer.oauth_token,
                    int(time.mktime((profile.last_changes).timetuple()))
                )
            else:
                path = 'https://graph.facebook.com/%s/locations?access_token=%s' % (
                    profile.fid, self.organizer.oauth_token
                )
            response = urllib2.urlopen(path)
            data = json.loads(response.read())

            profile_categories = json.loads(profile.categories_data) \
                if profile.categories_data else {}
            for checkin in data.get('data', []):
                if 'place' not in checkin:
                    # skip check-ins without place
                    continue
                logger.debug(
                    'Parsing check-in for place "%s"' % checkin['place']['name']
                )
                place_id = checkin['place']['id']
                path = 'https://graph.facebook.com/%s' % place_id
                response = urllib2.urlopen(path)
                data = json.loads(response.read())
                if not data:
                    logger.debug('Empty results for page %s' % place_id)
                    continue
                place_category = normalize_place_category(
                    data.get('category', ''),
                    data['name']
                )
                if place_category in VALID_PLACE_CATEGORIES:
                    # we are assuming that user have been 1 time
                    # in each type of places
                    profile_categories.setdefault(place_category, 1)
                    profile_categories[place_category] += 1

                    # # saving page info to database
                    # try:
                    #     place_obj = Place.objects.get(
                    #         fid=place_id
                    #     )
                    # except Place.DoesNotExist:
                    #     place_obj = Place(fid=place_id)
                    #     place_obj
                    #     place_obj.fid = place['id']
                    #     place_obj.category = place_category
                    #     place_obj.lat = place['location']['latitude']
                    #     place_obj.lon = place['location']['longitude']

            profile.last_changes = datetime.now()
            profile.categories_data = json.dumps(profile_categories)
            profile.categories = profile_categories
            profile.categories_count = sum(profile_categories.values())
            profile.save()
            logger.debug('Categories for user %s: %s' % (profile.fid, profile_categories))

        # going throw places in current radius and determining how good it's to
        # to each user

        max_likes_count = 1
        for place in places:
            if place.likes_count > max_likes_count:
                max_likes_count = place.likes_count

        self.status_events.create(
            message=_('Calculating recommendations...')
        )
        for place in places:
            place_result, c = PlanningResultPlace.objects.get_or_create(
                planning=self,
                place=place
            )
            place_result.category_rank = 0
            for profile in profiles:
                place_result.category_rank += \
                    float(profile.categories.get(place.category, 0)) / \
                    profile.categories_count if profile.categories_count \
                    else 0
            # normalization
            place_result.category_rank /= len(profiles)
            place_result.likes_rank = float(place.likes_count) / max_likes_count
            place_result.rank = place_result.likes_rank * place_result.category_rank
            place_result.save()

        self.status = self.STATUS_DONE
        self.percent = 100
        self.status_events.create(
            message=_('Done')
        )
        self.save()


class PlanningResultPlace(models.Model):
    planning = models.ForeignKey(Planning, related_name='results')
    place = models.ForeignKey(Place)
    category_rank = models.FloatField(default=0)
    likes_rank = models.FloatField(default=0)
    rank = models.FloatField(default=0)

    def __unicode__(self):
        return unicode(self.place)

    class Meta:
        unique_together = ('planning', 'place')
        ordering = ('-category_rank',)


class PlanningStatusEvent(models.Model):
    planning = models.ForeignKey(Planning, related_name='status_events')
    event_type = models.TextField(blank=True, null=True)
    message = models.TextField()

# class Similarity(models.Model):
#     place1 = models.ForeignKey(Place, related_name='similar_to')
#     place2 = models.ForeignKey(Place, related_name='similar_from')
#     rank = models.FloatField(default=0)
