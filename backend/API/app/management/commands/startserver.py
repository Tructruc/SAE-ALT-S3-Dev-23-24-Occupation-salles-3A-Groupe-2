import os
import logging
import threading
from django.core.management.base import BaseCommand
from django.core.management import call_command
from project.settings.dev_settings import DEFAULT_IP, DEFAULT_PORT
from app.processmqttlistenerstarter import start_process_mqtt_listener
from project.loggerconfig import setup_logger
from app.threadredislistenerstarter import start_thread_redis_listener

class Command(BaseCommand):
    help = 'Run the Django development server using environment variables for IP and port'

    def handle(self, *args, **kwargs):
        if os.environ.get('RUN_MAIN'):
            setup_logger()
            logging.getLogger('API').warning('You are in development mode ! \nSome logs are not enabled in certain files because they slow down the server. \nCheck the relevant file and uncomment the log if necessary')

            # Démarrer le listener Redis dans un thread
            start_thread_redis_listener()

            # Démarrer le process MQTT listener
            start_process_mqtt_listener()

        call_command('runserver', f'{DEFAULT_IP}:{DEFAULT_PORT}')
