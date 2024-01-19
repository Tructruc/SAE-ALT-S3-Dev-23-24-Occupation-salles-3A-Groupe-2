from project.loggerconfig import setup_logger, setup_gunicorn_loggers
from project.settings.prod_settings import DEFAULT_IP, DEFAULT_PORT

bind = f"{DEFAULT_IP}:{DEFAULT_PORT}"

def on_starting(server):
    custom_logger = setup_logger()
    setup_gunicorn_loggers(custom_logger)