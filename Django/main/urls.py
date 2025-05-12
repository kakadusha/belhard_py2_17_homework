"""
Локальный ЮРЛС
"""

from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index),
    path("", views.default_page),
    path("duck", views.duck),
    path("duck/", views.duck),
    path("fox/<int:num>", views.fox),
    path("fox/<int:num>/", views.fox),
    path("about", views.about),
]
