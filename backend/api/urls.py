from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.get_devices),
    path('devices/<int:device_id>/history/', views.device_history),
]