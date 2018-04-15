
from django.urls import path

from . import views

urlpatterns = [
            path('getControllers/<int:user_id>', views.getControllers, name='getControllers'),
            path('postControllers', views.insertControllers, name='postControllers'),
            path('getLogs/<str:mac>/<int:port_id>/<int:records_n>', views.getLogs, name='getLogs'),
            path('checkMac/<str:mac>', views.checkMac, name='checkMac'),
            path('setPorts', views.setPorts, name='setPorts')
            ]
