import importlib
import logging
import os

# from project.settings.base_settings import ColorFormatter, LOGGING_LEVEL
# from django.conf import settings
# from django.conf.global_settings import ColorFormatter, LOGGING_LEVEL

# Récupérer la valeur de la variable d'environnement
settings_module_name = os.environ.get('DJANGO_SETTINGS_MODULE')

if settings_module_name:
    # Importer le module de paramètres en utilisant le nom du module
    settings_module = importlib.import_module(settings_module_name)

    # Utiliser `getattr` pour accéder aux attributs par leur nom
    ColorFormatter = getattr(settings_module, 'ColorFormatter', None)
    LOGGING_LEVEL = getattr(settings_module, 'LOGGING_LEVEL', None)
    PATH_TO_LOG_FILE = getattr(settings_module, 'PATH_TO_LOG_FILE', None)

    if ColorFormatter is not None and LOGGING_LEVEL is not None:
        # Vous pouvez maintenant utiliser `ColorFormatter` et `LOGGING_LEVEL`
        print('DEBUG:', getattr(settings_module, 'DEBUG', None))
        print('ColorFormatter:', ColorFormatter)
        print('LOGGING_LEVEL:', LOGGING_LEVEL)
        print('PATH_TO_LOG_FILE:', PATH_TO_LOG_FILE)
    else:
        print("ColorFormatter ou LOGGING_LEVEL n'est pas défini dans le module des paramètres.")
else:
    print("La variable d'environnement DJANGO_SETTINGS_MODULE n'est pas définie.")


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