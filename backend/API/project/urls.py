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
from django.contrib import admin
from django.urls import include, path, re_path
from deepserializer import DeepViewSet
from app.models import Sensor, Data
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from app.usecases.mqttlistener import MqttClientThread

router = routers.DefaultRouter()
DeepViewSet.init_router(router, [
    Data,
    Sensor,
])

urlpatterns = [
    re_path(r'', include(router.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

import sys

if 'runserver' in sys.argv : # Only run the MQTT client when running the server
    print("Démarrage des threads MQTT")

    mqtt_thread_1 = MqttClientThread("application/1/device/+/event/status")
    mqtt_thread_1.daemon = True
    mqtt_thread_1.start()
    print("Thread 1 started")

    mqtt_thread_2 = MqttClientThread("AM107/by-room/#")
    mqtt_thread_2.daemon = True
    mqtt_thread_2.start()
    print("Thread 2 started")
