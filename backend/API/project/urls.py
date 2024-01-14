"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from deepserializer import DeepViewSet
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from app.views import DataViewSet, ByRoomViewSet, SensorViewSet
from app.processmqttlistenerstarter import start_process_mqtt_listener

router = routers.DefaultRouter()
DeepViewSet.init_router(router, [
])

router.register(r'Sensor', SensorViewSet, basename='Sensor')
router.register(r'Data', DataViewSet, basename='Data')
router.register(r'ByRoom', ByRoomViewSet, basename='ByRoom')


urlpatterns = [
    re_path(r'', include(router.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

import sys
from project.loggerconfig import setup_logger

if 'runserver' in sys.argv : # Start MQTT process and logger only if manage.py runserver is running (In development)
    setup_logger()
    start_process_mqtt_listener()