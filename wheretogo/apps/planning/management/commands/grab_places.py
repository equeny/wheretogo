import logging

from django.core.management.base import BaseCommand

from planning.models import Place

logger = logging.getLogger("wheretogo.%s" % __name__)


class Command(BaseCommand):
    args = 'lat, lon, radius, oauth_token'

    def handle(self, *args, **options):
        lat, lon, radius, token = args[0], args[1], args[2], args[3]

        Place.objects.grab_places(float(lat), float(lon), float(radius), token)
