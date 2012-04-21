from django.contrib import admin

from planning.models import Planning, Place, PlanningResultPlace


admin.site.register(Planning)
admin.site.register(Place)
admin.site.register(PlanningResultPlace)
