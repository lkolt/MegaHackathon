
from django.urls import path

from . import views

urlpatterns = [
            path('getControllers/<int:user_id>', views.getControllers, name='getControllers'),
            path('insertTest', views.insertTest, name='insertShit'),
            path('postControllers', views.insertControllers, name='postControllers')
            ]
