from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .models import Route


class IndexView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'main/index.html'
    context_object_name = 'route'

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related('points').order_by('?').first()

    @method_decorator(cache_page(60*60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PointsListView(LoginRequiredMixin, View):

    def get(self, *args, **kw):
        route = get_object_or_404(Route, pk=kw.get('route_pk'))
        return JsonResponse({'data': route.formatted_points})

    @method_decorator(cache_page(60*60))
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

