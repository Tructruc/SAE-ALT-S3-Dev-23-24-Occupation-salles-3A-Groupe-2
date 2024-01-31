import logging
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Data, Sensor
from app.usecases.redis import redis_sender
from django.core import serializers

logger = logging.getLogger('API')

@receiver(post_save, sender=Sensor)
def sensor_post_save(sender, instance, **kwargs):
    pass