# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(is_safe=True)
def distance(self, other):
    """Расчет расстояния между точками (в километрах)"""
    return round(self.location.distance(other.location) * 100)
