from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from .models import Route, RoutePoint


class IndexView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'main/index.html'
    context_object_name = 'route'

    def get_object(self, queryset=None):
        return self.model.objects.order_by('?').first()


class PointsListView(LoginRequiredMixin, View):

    def get(self, *args, **kw):
        response = dict(points=[])
        route = get_object_or_404(Route, pk=kw.get('route_pk'))
        for p in route.points.all():
            point = dict(location=p.location.get_coords())
            point['name'] = p.name
            point['description'] = p.description
            response['points'].append(point)
        return JsonResponse({'data': response})

