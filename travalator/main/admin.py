from django.contrib import admin
from .models import Point, Route, RoutePointM2M, CompanyPoint, AdminPoint, SavedRoutes


class RoutePontM2MInline(admin.TabularInline):
    model = RoutePointM2M
    extra = 0


class SavedRoutesM2MInline(admin.TabularInline):
    model = SavedRoutes
    extra = 0


@admin.register(Point)
class RoutePointAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = (RoutePontM2MInline, SavedRoutesM2MInline)


@admin.register(CompanyPoint)
class CompanyPointAdmin(admin.ModelAdmin):
    pass


@admin.register(AdminPoint)
class AdminPointAdmin(admin.ModelAdmin):
    pass
