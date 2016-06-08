from django.contrib import admin
from .models import RoutePoint, Route

# Register your models here.


@admin.register(RoutePoint)
class RoutePointAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass
