import logging
import os

from project.settings import ColorFormatter, LOGGING_LEVEL


def setup_logger():
    """
    This method is used to setup the logger for the API.
    """
    logger = logging.getLogger('API') # The name of the logger is API
    logger.setLevel(LOGGING_LEVEL) # The level of the logger is the one defined in the settings
    logger.propagate = False # The logger does not propagate to the parent logger

    # If the log file don't exist, we create it
    if not os.path.isfile('/back-end/api.log'):
        open('/back-end/api.log', 'a').close()

    # Add a file handler to the logger to save the logs in a file
    file_handler = logging.FileHandler('/back-end/api.log', mode='a')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Add a stream handler to the logger to print the logs in the console with colors from the ColorFormatter class
    stream_handler = logging.StreamHandler()
    stream_formatter = ColorFormatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger