from django.contrib import admin

from planning.models import Planning, Place, PlanningResultPlace


class PlanningAdmin(admin.ModelAdmin):
    actions = ['find_where_to_go']

    def find_where_to_go(self, request, queryset):
        for planning in queryset:
            planning.find_where_to_go()


admin.site.register(Planning, PlanningAdmin)
admin.site.register(Place)
admin.site.register(PlanningResultPlace)
