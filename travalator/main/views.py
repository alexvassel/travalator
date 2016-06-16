from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from .models import Route


class IndexView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'main/index.html'
    context_object_name = 'route'

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related('points').order_by('?').first()


class PointsListView(LoginRequiredMixin, View):

    def get(self, *args, **kw):
        route = get_object_or_404(Route, pk=kw.get('route_pk'))
        return JsonResponse({'data': route.formatted_points})

