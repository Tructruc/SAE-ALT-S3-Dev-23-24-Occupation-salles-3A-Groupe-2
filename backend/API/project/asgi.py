"""
ASGI config for API project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from app.processmqttlistenerstarter import start_process_mqtt_listener

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()

import sys
from project.loggerconfig import setup_logger

if '/usr/local/bin/gunicorn' in sys.argv : # Start MQTT process and logger only if gunicorn is running (In production)
    start_process_mqtt_listener()
    logger = setup_logger()
