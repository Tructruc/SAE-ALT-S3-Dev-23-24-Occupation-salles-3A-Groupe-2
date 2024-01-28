import multiprocessing
import os

from project.loggerconfig import setup_logger, setup_gunicorn_loggers
from project.settings.prod_settings import DEFAULT_IP, DEFAULT_PORT, CERTFILE, KEYFILE
from app.processmqttlistenerstarter import start_process_mqtt_listener
from django.core.wsgi import get_wsgi_application


bind = f"{DEFAULT_IP}:{DEFAULT_PORT}"
custom_logger = setup_logger()
workers = multiprocessing.cpu_count() * 2 + 1
certfile = CERTFILE
keyfile = KEYFILE

def on_starting(server):
    setup_gunicorn_loggers(custom_logger)    

def when_ready(server):
    custom_logger.info("Starting MQTT listener process")
    os.environ.get("DJANGO_SETTINGS_MODULE")
    get_wsgi_application()
    start_process_mqtt_listener()