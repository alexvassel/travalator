from itertools import tee

from django.contrib.gis.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from location_field.models.spatial import LocationField
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField

from ..users.models import Tourist, Company, User


class DescriptionedModel(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, default='')
    description = HTMLField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Route(DescriptionedModel):
    points = models.ManyToManyField('Point', through='RoutePointM2M', verbose_name=_('points'))
    center = LocationField(verbose_name=_('center'), based_fields=['name'],
                           default='POINT(0.0 0.0)')
    saved_by = models.ManyToManyField(Tourist, through='SavedRoutes', blank=True,
                                      related_name='saved_by', verbose_name=_('saved_by'))
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name=_('tourist'))
    popularity = models.PositiveIntegerField(_('popularity'), blank=True, null=True)
    cost = models.PositiveIntegerField(_('cost'), blank=True, null=True)
    extremality = models.PositiveSmallIntegerField(_('extremality'), blank=True, null=True)

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
        """iterable -> (iterable[0], iterable[1]), (iterable[1], iterable[2]), ...)"""
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    @cached_property
    def tourist_points(self):
        return self.points.filter(companypoint__isnull=True, adminpoint__isnull=True)

    @cached_property
    def company_points(self):
        return self.points.filter(companypoint__isnull=False, adminpoint__isnull=True)

    @cached_property
    def admin_points(self):
        return self.points.filter(adminpoint__isnull=False, companypoint__isnull=True)

    def __str__(self):
        return self.name


class Point(DescriptionedModel):
    location = LocationField(based_fields=['name'], default='POINT(0.0 0.0)',
                             verbose_name=_('location'))
    phone = PhoneNumberField(_('phone'), max_length=12)

    objects = models.GeoManager()

    class Meta:
        ordering = ('routepointm2m__point_number',)


class CompanyPoint(Point):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))

    objects = models.GeoManager()


class AdminPoint(Point):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('admin'))

    objects = models.GeoManager()


class RoutePointM2M(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE, verbose_name=_('point'))
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name=_('route'))
    point_number = models.PositiveIntegerField(blank=True, null=True,
                                               verbose_name=_('point number'))

    def __str__(self):
        return str()

    class Meta:
        verbose_name_plural = 'Points'


class SavedRoutes(TimeStampedModel):
    route = models.ForeignKey(Route, verbose_name=_('route'))
    tourist = models.ForeignKey(Tourist, verbose_name=_('tourist'))

    def __str__(self):
        return str()

    class Meta:
        verbose_name_plural = 'Saved by'
        verbose_name = 'Saved by'
