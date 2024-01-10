from django.apps import AppConfig
from app.usecases.mqttlistener import MqttClientThread


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'