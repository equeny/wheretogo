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

    def __unicode__(self):
        return u'Facebook user for %s' % self.user


def new_users_handler(sender, user, response, details, **kwargs):
    FacebookProfile.objects.create(user=user, fid=response['id'])
    return False
