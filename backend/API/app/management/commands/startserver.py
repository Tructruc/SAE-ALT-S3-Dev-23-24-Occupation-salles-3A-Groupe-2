import os
import logging
import threading
from django.core.management.base import BaseCommand
from django.core.management import call_command
from project.settings.dev_settings import DEFAULT_IP, DEFAULT_PORT
from app.processmqttlistenerstarter import start_process_mqtt_listener
from project.loggerconfig import setup_logger
from app.usecases.redislistener import redis_listener

class Command(BaseCommand):
    help = 'Run the Django development server using environment variables for IP and port'

    def start_redis_listener_thread(self):
        # Créez et démarrez le thread pour le listener Redis
        thread = threading.Thread(target=redis_listener, args=('sse',))
        thread.daemon = True  # Cela permet au thread de s'arrêter avec le programme
        thread.start()

    def handle(self, *args, **kwargs):
        if os.environ.get('RUN_MAIN'):
            setup_logger()
            logging.getLogger('API').warning('You are in development mode ! \nSome logs are not enabled in certain files because they slow down the server. \nCheck the relevant file and uncomment the log if necessary')

            # Démarrer le listener Redis dans un thread
            self.start_redis_listener_thread()

            # Démarrer le process MQTT listener
            start_process_mqtt_listener()

        call_command('runserver', f'{DEFAULT_IP}:{DEFAULT_PORT}')
