import importlib
import logging
import os

# Get the settings module name from the environment variable
settings_module_name = os.environ.get('DJANGO_SETTINGS_MODULE')

if settings_module_name:
    # Import dynamiclly the settings module to be able to get tje current settings
    settings_module = importlib.import_module(settings_module_name)

    # Use getattr to get the value of the variable in the settings module that we need here
    ColorFormatter = getattr(settings_module, 'ColorFormatter', None)
    LOGGING_LEVEL = getattr(settings_module, 'LOGGING_LEVEL', None)
    PATH_TO_LOG_FILE = getattr(settings_module, 'PATH_TO_LOG_FILE', None)

    if not ColorFormatter or not LOGGING_LEVEL or not PATH_TO_LOG_FILE:
        raise ValueError('Some variables are missing in the settings module, app cannot start properly.')
else:
    raise ValueError('DJANGO_SETTINGS_MODULE variable is not set in the environment.')


def setup_gunicorn_loggers(logger):
    """
    Configure Gunicorn loggers to use the same handlers as our custom logger.
    """
    # Configure Gunicorn error logger
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    gunicorn_error_logger.handlers = logger.handlers
    gunicorn_error_logger.setLevel(logger.level)


def setup_logger():
    """
    This method is used to setup the logger for the API.
    """
    logger = logging.getLogger('API') # The name of the logger is API
    logger.setLevel(LOGGING_LEVEL) # The level of the logger is the one defined in the settings
    logger.propagate = False # The logger does not propagate to the parent logger



    # If the log file don't exist, we create it
    if not os.path.isfile(PATH_TO_LOG_FILE):
        open(PATH_TO_LOG_FILE, 'a').close()

    # Add a file handler to the logger to save the logs in a file
    file_handler = logging.FileHandler(PATH_TO_LOG_FILE, mode='a')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Add a stream handler to the logger to print the logs in the console with colors from the ColorFormatter class
    stream_handler = logging.StreamHandler()
    stream_formatter = ColorFormatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger
