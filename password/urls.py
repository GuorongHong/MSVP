from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_pw/', views.add_pw, name='add_pw')
]