from itertools import tee

from django.contrib.gis.db import models
from django.utils.functional import cached_property

from location_field.models.spatial import LocationField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from ..users.models import User


class DescriptionedModel(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, default='')
    description = HTMLField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Point(DescriptionedModel):
    location = LocationField(based_fields=['name'], default='POINT(0.0 0.0)')

    objects = models.GeoManager()

    class Meta:
        ordering = ('routepointm2m__point_number',)


class AgencyPoint(Point, UserModel):
    objects = models.GeoManager()


class Route(DescriptionedModel, UserModel):
    points = models.ManyToManyField(Point, through='RoutePointM2M')
    center = LocationField(based_fields=['name'], default='POINT(0.0 0.0)')

    objects = models.GeoManager()

    @cached_property
    def formatted_points(self):
        data = dict(points=[])
        for p in self.tourist_points:
            point = dict(location=p.location.get_coords())
            point['name'] = p.name
            point['description'] = p.description
            data['points'].append(point)
        return data

    @cached_property
    def length(self):
        # километры
        length = sum(a.location.distance(b.location)
                     for (a, b) in self._pairwise(self.tourist_points)) * 100
        return round(length)

    @cached_property
    def pairwised_points(self):
        """route.points.all() -> (point0, points1), (point1, point2), (point2, point3), ..."""
        return self._pairwise(self.tourist_points)

    @staticmethod
    def _pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    @cached_property
    def tourist_points(self):
        return self.points.filter(agencypoint=None)

    def __str__(self):
        return self.name


class RoutePointM2M(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    root = models.ForeignKey(Route, on_delete=models.CASCADE)
    point_number = models.PositiveIntegerField(blank=True, null=True)
