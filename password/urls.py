from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_pw/', views.add_pw, name='add_pw'),
    path('<int:id>/delete/', views.del_pw, name="del_pw"),
    path('generate_pw/', views.generate_pw, name="generate_pw"),
    path('verify_pw/', views.verify_pw, name='verify_pw'),
]