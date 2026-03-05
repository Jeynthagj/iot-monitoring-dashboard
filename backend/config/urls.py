from django.contrib import admin#import admin module to register models in admin interface
from django.urls import path#import path function to define url patterns
from api.views import get_devices#import the view to get device data

urlpatterns = [
    path('admin/', admin.site.urls),#admin page
    path('api/devices/', get_devices),#api endpoint to get device data
]