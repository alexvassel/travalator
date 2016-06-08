from django.contrib import admin
from .models import RoutePoint, Route, RoutePointM2M


class RoutePontM2MInline(admin.TabularInline):
    model = RoutePointM2M
    extra = 1


@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    inlines = (RoutePontM2MInline,)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = (RoutePontM2MInline,)
