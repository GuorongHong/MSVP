from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('hint/', views.login_hint, name='login_hint'),
    path('hint/edit/', views.add_hint, name='add_hint'),
    path('email/edit/', views.change_email, name='change_email'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]