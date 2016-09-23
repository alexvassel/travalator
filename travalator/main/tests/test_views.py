import http.client

from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.test import RequestFactory

from test_plus.test import TestCase

from ..tests.factories import RouteWith3PointsFactory
from ..views import IndexView, PointsListView


class TestRoute(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
        self.route = RouteWith3PointsFactory()
        self.index_url = 'main:index'
        self.points_url = 'main:route_points'

    def test_not_logged_in(self):
        self.assertLoginRequired(self.index_url)

    def test_route(self):
        request = self.factory.get(reverse(self.index_url))
        request.user = self.user
        response = IndexView.as_view()(request)
        self.assertEquals(response.status_code, http.client.OK)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(IndexView().get_object(), self.route)

    def test_points(self):
        request = self.factory.get(reverse(self.points_url, kwargs={'route_pk': self.route.pk}))
        request.user = self.user
        response = PointsListView.as_view()(request, route_pk=self.route.pk)
        self.assertEquals(response.status_code, http.client.OK)

