import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger("wheretogo.%s" % __name__)


class FacebookProfile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True,
        verbose_name=_('User'), related_name='fb_user'
    )
    users = models.ManyToManyField(User, related_name='friends',)
    fid = models.CharField(_('Facebook id'), max_length=50)
    name = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)
    oauth_token = models.TextField(_('oauth_token'), null=True, blank=True)
    categories_data = models.TextField(blank=True, null=True)
    categories_count = models.PositiveIntegerField(default=0)
    last_changes = models.DateTimeField(
        _('Last changes date'), blank=True, null=True
    )
    last_friends_update = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.name


def new_users_handler(sender, user, response, details, **kwargs):
    profile, c = FacebookProfile.objects.get_or_create(user=user, fid=response['id'])
    profile.oauth_token = response['access_token']
    profile.name = response['name']
    profile.save()
    return False
