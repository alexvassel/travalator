from django.contrib import admin
from .models import RoutePoint

# Register your models here.


class RoutePointAdmin(admin.ModelAdmin):
    pass

admin.site.register(RoutePoint, RoutePointAdmin)
