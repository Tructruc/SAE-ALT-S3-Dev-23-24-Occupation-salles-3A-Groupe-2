import json
import redis
import logging

from django_eventstream import send_event

logger = logging.getLogger('API')

def redis_listener(stop_event):
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    listener = r.pubsub()
    listener.subscribe('sse')

    for message in listener.listen():
        if stop_event.is_set():
            break
        if message['type'] == 'message':
            message_decode = message['data'].decode('utf-8').replace('"', "").replace("'", '"')
            logger.debug(f"Message redis reçu: {message_decode}")

            message_data = json.loads(message_decode)
            logger.debug(f"Message redis reçu: {message_data}")

            if 'Data' in message_data['type']:
                logger.debug("Data received from Redis")
                formatted_message = message_data['message']
                send_event(message_data['type'], 'message', formatted_message)
                logger.debug(f"Event sent on {message_data['type']}")

            elif 'Sensor' in message_data['type']:
                logger.debug("Sensor received from Redis")
                formatted_message = message_data['message']
                logger.debug(f"Event sent on Sensor")
                send_event('Sensor', 'message', formatted_message)

    listener.unsubscribe('sse')
    logger.info("Redis listener stopped")
