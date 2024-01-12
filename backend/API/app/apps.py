from django.apps import AppConfig

import os, sys, logging

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'