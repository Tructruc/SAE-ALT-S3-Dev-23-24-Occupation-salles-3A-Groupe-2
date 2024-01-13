from .base_settings import *

SECRET_KEY = 'django-insecure-^m^9b2&$=(#u2zs4+%-4mr)sf3h-8w(cb_@o7r&-hvh76o5d4u'
DEBUG = False
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ['localhost', "localhost:8080", "http://localhost:8080"]

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
