from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import DetailView

from .models import Route


class IndexView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'main/index.html'

    def get_object(self, queryset=None):
        return self.model.objects.order_by('?').first()
