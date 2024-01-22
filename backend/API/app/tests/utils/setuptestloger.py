import importlib
import logging
import os

def setup_logger():
    """
    This method is used to setup the logger for the API.
    """
    logger = logging.getLogger('TEST') # The name of the logger is API
    logger.setLevel(logging.DEBUG) # The level of the logger is the one defined in the settings
    logger.propagate = False # The logger does not propagate to the parent logger
    
    # Add a stream handler to the logger to print the logs in the console with colors from the ColorFormatter class
    stream_handler = logging.StreamHandler()
    stream_formatter = ColorFormatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger

class ColorFormatter(logging.Formatter):
    # Codes de couleur ANSI
    COLORS = {
        'WARNING': '\033[93m', # Jaune
        'INFO': '\033[94m',    # Bleu
        'DEBUG': '\033[92m',   # Vert
        'CRITICAL': '\033[91m',# Rouge
        'ERROR': '\033[91m',   # Rouge
        'ENDC': '\033[0m',     # Fin de la couleur
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname_color = self.COLORS[levelname] + levelname + self.COLORS['ENDC']
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)
