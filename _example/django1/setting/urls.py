"""
URL configuration for setting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path

# from app1.views import index, hello2, hello3, user_num
# from app1 import views
from main.views import *


urlpatterns = [
    path("", index, name="index"),
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("students/", students, name="students"),
    path("students2/", StudentsView.as_view(), name="students2"),
    # path("students/<int:id>", StudentsView.as_view, name="students2"),
]


"""
ТИПЫ ПАРАМЕТРОВ
str — любая непустая строка без символа /
int — положительное целое число
slug — буквы, цифры, дефисы и подчёркивания
uuid — UUID
path — строка, может содержать символ /"""
