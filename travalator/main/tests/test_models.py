from test_plus.test import TestCase

from .factories import RouteWith3PointsFactory, RoutePointM2MFactory
from ..templatetags.helpers import distance


class TestRoute(TestCase):
    LENGTH = {'route': 85, 'parts': {'first': 32, 'second': 53}}
    POINTS_COUNT = {'admin': 0, 'company': 0, 'tourist': 3}

    def setUp(self):
        # Сбрасываем счетчик, чтобы снова начинать с 0 перед каждым тестом
        RoutePointM2MFactory.reset_sequence()
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
        self.assertEquals(self.route.tourist_points.count(), self.POINTS_COUNT['tourist'])

    def test_company_points_count(self):
        self.assertEquals(self.route.company_points.count(), self.POINTS_COUNT['company'])

    def test_admin_points_count(self):
        self.assertEquals(self.route.admin_points.count(), self.POINTS_COUNT['admin'])

    def test_points_order(self):
        # Порядок у точек верный
        for i, line in enumerate(self.route.routepointm2m_set.all(), start=1):
            self.assertEquals(i, line.point_number)

    def test_points_formatting(self):
        # На выходе правильный словарь
        formatted = self.route.formatted_points
        self.assertIsInstance(formatted, dict)
        key = ['points']
        self.assertEquals(set(key), set(formatted))
        self.assertEquals(len(formatted[key[0]]), self.POINTS_COUNT['tourist'])
        self.assertIsInstance(formatted[key[0]], list)

        for point in formatted[key[0]]:
            self.assertIsInstance(point, dict)
            expected_keys = ['name', 'description', 'location']
            self.assertEquals(set(expected_keys), set(point))

