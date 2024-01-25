import dj_database_url
import logging

SECRET_KEY = 'django-insecure-^m^9b2&$=(#u2zs4+%-4mr)sf3h-8w(cb_@o7r&-hvh76o5d4u'
DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
TIME_ZONE = 'Europe/Paris'

ALLOWED_HOSTS = ['localhost', 'localhost:8080', 'localhost:5173', "http://localhost:8080", "http://localhost:5173"]

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:postgres@localhost:5432/data-iot')
}