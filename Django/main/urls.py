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
    path("students/", views.students, name="students"),
    path("students/<int:id>/", views.student, name="student"),
    path("students2/", views.StudentsView.as_view(), name="students2"),
    path("students2/<slug:name_slug>/", views.StudentView.as_view(), name="student2"),
    path("login/", views.login, name="login"),
]
