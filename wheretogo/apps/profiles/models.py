from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class FacebookProfile(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True,
        verbose_name=_('User')
    )

    fid = models.CharField(_('Facebook id'), max_length=50)
