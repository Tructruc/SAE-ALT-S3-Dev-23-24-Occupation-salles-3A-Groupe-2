import multiprocessing
import os

from project.loggerconfig import setup_logger, setup_gunicorn_loggers
from project.settings.prod_settings import DEFAULT_IP, DEFAULT_PORT#, CERTFILE, KEYFILE
from app.processmqttlistenerstarter import start_process_mqtt_listener
from app.threadredislistenerstarter import start_thread_redis_listener
from django.core.wsgi import get_wsgi_application


bind = f"{DEFAULT_IP}:{DEFAULT_PORT}"
custom_logger = setup_logger()
workers = multiprocessing.cpu_count() * 2 
# certfile = CERTFILE
# keyfile = KEYFILE

def on_starting(server):
    setup_gunicorn_loggers(custom_logger)    
    get_wsgi_application()

def when_ready(server):
    custom_logger.info("Starting MQTT listener process")
    os.environ.get("DJANGO_SETTINGS_MODULE")
    mqttlisteners = start_process_mqtt_listener()
    server.mqttlisteners = mqttlisteners

def post_fork(server, worker):
    worker_id = worker.pid
    custom_logger.info(f"Starting Redis listener in worker {worker_id}")
    thread, stop_event = start_thread_redis_listener()
    worker.redis_listener_thread = thread
    worker.redis_stop_event = stop_event
    custom_logger.info(f"Redis listener running in worker {worker_id}")

def worker_exit(server, worker):
    worker.redis_stop_event.set()
    worker.redis_listener_thread.join()
    custom_logger.info(f"Redis listener stopped in worker {worker.pid}")


def on_exit(server):
    custom_logger.info("Stopping MQTT listener process")
    for listener in server.mqttlisteners:
        listener.stop()
    custom_logger.info("MQTT listener process stopped")