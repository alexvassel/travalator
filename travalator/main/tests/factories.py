# -*- coding: utf-8 -*-
import factory

from ..models import Route, Point, RoutePointM2M
from ...users.tests.factories import TouristFactory


class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Route

    tourist = factory.SubFactory(TouristFactory)
    name = factory.Sequence(lambda n: 'Route {}'.format(n + 1))


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point


class RoutePointM2MFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutePointM2M

    point = factory.SubFactory(PointFactory)
    route = factory.SubFactory(RouteFactory)
    point_number = factory.Sequence(lambda n: n + 1)


class RouteWith2PointsFactory(RouteFactory):
    m = factory.RelatedFactory(RoutePointM2MFactory, 'route', point__name='m',
                               point__location='POINT(37.765499 55.919847)')
    h = factory.RelatedFactory(RoutePointM2MFactory, 'route', point__name='h',
                               point__location='POINT(37.443949 55.894055)')
