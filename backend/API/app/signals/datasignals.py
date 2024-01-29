import logging
import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Data, Sensor
from app.usecases.redis import redis_sender
from django.core import serializers

logger = logging.getLogger('API')

@receiver(post_save, sender=Data)
def data_post_save(sender, instance, **kwargs):
    logger.info("Data savedddd !!!!")

    json_data = serializers.serialize('json', [instance])
    
    data_dict = json.loads(json_data)

    fields_data = data_dict[0]['fields']
    
    sensor = Sensor.objects.get(deveui=fields_data['sensor'])
    
    fields_data.pop('sensor', None)
    
    fields_data_json = json.dumps(fields_data)

    redis_sender(f'Data/{sensor.room}', fields_data)

    logger.info("Data sent to Redis !!!!")
