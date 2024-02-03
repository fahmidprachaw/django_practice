from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('singup/', views.Singup, name='singup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.singn_out, name='logout'),
    path('profile/', views.Profile, name='profile'),
    path('passchange/', views.change_password, name='passchange'),
]