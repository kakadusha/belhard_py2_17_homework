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
    # path("students/", views.students, name="students"),
    # path("students/<int:id>/", views.student, name="student"),
    path("students/", views.StudentsView.as_view(), name="students"),
    path("students/<slug:name_slug>/", views.StudentView.as_view(), name="student"),
    path("cources/", views.under_constuction, name="cources"),
    path("cources/<slug:name_slug>/", views.under_constuction, name="cources"),
    path("grades/", views.under_constuction, name="grades"),
    path("grades/<slug:name_slug>/", views.under_constuction, name="grades"),
    path("login/", views.login, name="login"),
]
