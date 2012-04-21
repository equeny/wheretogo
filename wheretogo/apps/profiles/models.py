import logging
import urllib
import urllib2
import json

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger("wheretogo.%s" % __name__)


class FacebookProfile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True,
        verbose_name=_('User')
    )

    fid = models.CharField(_('Facebook id'), max_length=50)
    oauth_token = models.TextField(_('oauth_token'), null=True, blank=True)
    categories_data = models.TextField(blank=True, null=True)
    categories_count = models.PositiveIntegerField(default=0)
    last_change = models.DateField(
        _('Last change date'), blank=True, null=True
    )

    def __unicode__(self):
        return u'Facebook user for %s' % self.user


def new_users_handler(sender, user, response, details, **kwargs):
    profile, c = FacebookProfile.objects.get_or_create(user=user, fid=response['id'])
    profile.oauth_token = response['access_token']
    profile.save()
    return False
