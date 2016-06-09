# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from jsonview.decorators import json_view

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'
    ),

    url(
        regex=r'^route/(?P<route_pk>[0-9]+)/points/$',
        view=json_view(views.PointsListView.as_view()),
        name='route_points'
    ),

]
