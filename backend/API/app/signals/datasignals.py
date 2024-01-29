import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Data
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger('API')

@receiver(post_save, sender=Data)
def data_post_save(sender, instance, **kwargs):
    import multiprocessing
    print(multiprocessing.current_process().pid)
    logger.info("Data savedddd !!!!")
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_send)('sse', {
    #     'type': 'Data',
    #     'message': 'hello world'
    # })
    logger.info("Data saved !!!!")
    

    
    