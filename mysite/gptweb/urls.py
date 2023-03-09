from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('search',views.Search,name='search'),
    path('login',views.Login,name='login'),
    path('register',views.Register,name="register"),
    path('result', views.AnswerPage, name="result"),
    path('',views.Index,name='index'),
]