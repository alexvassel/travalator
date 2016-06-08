from django.contrib.gis.db import models

from location_field.models.spatial import LocationField
from tinymce.models import HTMLField

from ..users.models import User


class RoutePoint(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    location = LocationField(based_fields=['name'], zoom=7, default='POINT(0.0 0.0)')
    description = HTMLField(default='', blank=True)
    user = models.ForeignKey(User)

    objects = models.GeoManager()

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    description = HTMLField(default='', blank=True)
    points = models.ManyToManyField(RoutePoint, blank=True, null=True, through='RoutePontM2M')
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class RoutePontM2M(models.Model):
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE)
    root = models.ForeignKey(Route, on_delete=models.CASCADE)
    point_number = models.PositiveIntegerField()
