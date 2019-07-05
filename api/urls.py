from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.ListPassword.as_view()),
    path('<int:id>/', views.DetailPassword.as_view()),
    path('rest-auth/', include('rest_auth.urls')),
]