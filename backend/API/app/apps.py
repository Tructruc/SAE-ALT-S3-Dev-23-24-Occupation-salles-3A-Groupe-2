from django.apps import AppConfig
from app.usecases.mqttlistener import MqttClientThread


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            print("go")
            mqtt_thread_1 = MqttClientThread("application/1/device/+/event/status")
            print("la")
            mqtt_thread_1.start()
            print("laal")

            print("gogo")
            mqtt_thread_2 = MqttClientThread("AM107/by-room/#")
            mqtt_thread_2.start()