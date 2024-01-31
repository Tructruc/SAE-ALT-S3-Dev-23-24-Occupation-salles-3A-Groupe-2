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
    json_data = serializers.serialize('json', [instance])

    data_dict = json.loads(json_data)

    fields_data = data_dict[0]['fields']

    fields_data.pop('room', None)
    fields_data.pop('building', None)
    fields_data.pop('floor', None)

    redis_sender(f'Sensor/', fields_data)