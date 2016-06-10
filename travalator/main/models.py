from itertools import tee

from django.contrib.gis.db import models

from location_field.models.spatial import LocationField
from tinymce.models import HTMLField

from ..users.models import User


class RoutePoint(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    location = LocationField(based_fields=['name'], default='POINT(0.0 0.0)')
    description = HTMLField(default='', blank=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('routepointm2m__point_number',)


class Route(models.Model):
    name = models.CharField(max_length=255, blank=True, default='')
    description = HTMLField(default='', blank=True)
    points = models.ManyToManyField(RoutePoint, through='RoutePointM2M')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    center = LocationField(based_fields=['name'], default='POINT(0.0 0.0)')

    objects = models.GeoManager()

    @property
    def length(self):
        # километры
        return sum(a.location.distance(b.location)
                   for (a, b) in self._pairwise(self.points.all())) * 100

    @staticmethod
    def _pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def __str__(self):
        return self.name


class RoutePointM2M(models.Model):
    point = models.ForeignKey(RoutePoint, on_delete=models.CASCADE)
    root = models.ForeignKey(Route, on_delete=models.CASCADE)
    point_number = models.PositiveIntegerField()
