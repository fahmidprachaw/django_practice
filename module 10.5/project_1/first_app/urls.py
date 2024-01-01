from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home),
    path('result/', views.Result),
    path('course/', views.Courses),
]