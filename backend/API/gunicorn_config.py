import os
import multiprocessing
import threading

from project.loggerconfig import setup_logger, setup_gunicorn_loggers
from app.processmqttlistenerstarter import start_process_mqtt_listener

bind = "0.0.0.0:8000"
# workers = multiprocessing.cpu_count() * 2 + 1

def when_ready(server):
    custom_logger = setup_logger()
    setup_gunicorn_loggers(custom_logger)