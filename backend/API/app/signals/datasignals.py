import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Data
from app.usecases.redis import redis_sender

logger = logging.getLogger('API')

@receiver(post_save, sender=Data)
def data_post_save(sender, instance, **kwargs):
    import multiprocessing
    print(multiprocessing.current_process().pid)
    logger.info("Data savedddd !!!!")
    redis_sender('Data',instance)
    logger.info("Data saved !!!!")
    

    
    