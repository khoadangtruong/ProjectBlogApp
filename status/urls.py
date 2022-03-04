from django.urls import path

from .import views

urlpatterns = [
    path('health_check/', views.health_check_func, name = 'health_check')
]