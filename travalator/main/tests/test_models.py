from test_plus.test import TestCase

from .factories import RouteWith3PointsFactory
from ..templatetags.helpers import distance


class TestRoute(TestCase):
    LENGTH = {'route': 85, 'parts': {'first': 32, 'second': 53}}

    def setUp(self):
        self.route = RouteWith3PointsFactory()

    def test_route_lines_count(self):
        # Количество стрелок == (количеству точек - 1)
        self.assertEquals(len(list(self.route.pairwised_points)), self.route.points.count() - 1)

    def test_route_length(self):
        self.assertEquals(self.route.length, self.LENGTH['route'])

    def test_route_parts_length(self):
        parts = list(self.route.pairwised_points)
        self.assertEquals(distance(*parts[0]), self.LENGTH['parts']['first'])
        self.assertEquals(distance(*parts[1]), self.LENGTH['parts']['second'])

    def test_tourist_points_count(self):
        self.assertEquals(self.route.tourist_points.count(), 3)

    def test_company_points_count(self):
        self.assertEquals(self.route.company_points.count(), 0)

    def test_admin_points_count(self):
        self.assertEquals(self.route.admin_points.count(), 0)
