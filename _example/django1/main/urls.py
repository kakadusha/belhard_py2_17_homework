
from django.contrib import admin
from django.urls import path, include, re_path
# from app1.views import index, hello2, hello3, user_num
# from app1 import views
from main.views import *


urlpatterns = [
    path('students/', students, name='students'),
    path('students/<int:id>/', student, name='student'),
    
    path('students2/', StudentsView.as_view(), name='students2'),
    path('students2/<slug:name_slug>/', StudentView.as_view(), name='student2'),
    
    path('login/', login, name='login'),
    
]

