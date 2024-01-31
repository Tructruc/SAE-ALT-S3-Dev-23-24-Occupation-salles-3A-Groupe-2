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
    logger.debug("Data save, signal received")

    json_data = serializers.serialize('json', [instance])
    
    data_dict = json.loads(json_data)

    fields_data = data_dict[0]['fields']
    
    sensor = Sensor.objects.get(deveui=fields_data['sensor'])
    
    fields_data.pop('sensor', None)
    
    

    if sensor.room is not None:
        redis_sender(f'Data', {"room" : sensor.room, "data" : fields_data})
        logger.debug("Data")

        redis_sender(f'Data/{sensor.room}/', fields_data)
        logger.debug(f"Data/{sensor.room}/")

    if sensor.building is not None and sensor.room is not None :
        redis_sender(f'Data/{sensor.building}/', {"room" : sensor.room, "data" : fields_data})
        logger.debug(f"Data/{sensor.building}/")
    
    if sensor.floor is not None and sensor.building is not None and sensor.room is not None:
        redis_sender(f'Data/{sensor.building}/{sensor.floor}/', {"room" : sensor.room, "data" : fields_data})
        logger.debug(f"Data/{sensor.building}/{sensor.floor}/")

    logger.debug(f"Data sent to Redis on {sensor.room}")
