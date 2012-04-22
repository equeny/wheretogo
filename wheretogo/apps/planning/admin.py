from django.contrib import admin

from planning.models import Planning, Place, PlanningResultPlace


class PlanningAdmin(admin.ModelAdmin):
    actions = ['find_where_to_go']

    def find_where_to_go(self, request, queryset):
        for planning in queryset:
            planning.find_where_to_go()


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'likes_count')


class PlanningResultPlaceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'rank', 'likes_rank', 'category_rank')


admin.site.register(Planning, PlanningAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlanningResultPlace, PlanningResultPlaceAdmin)
