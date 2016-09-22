# -*- coding: utf-8 -*-
import factory

from ..models import Route

from ...users.tests.factories import TouristFactory


class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Route
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'name-{0}'.format(n))
    tourist = factory.SubFactory(TouristFactory)
