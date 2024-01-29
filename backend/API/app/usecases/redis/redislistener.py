import json
import redis

from asgiref.sync import async_to_sync
from django_eventstream import send_event

def redis_listener():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    listener = r.pubsub()
    listener.subscribe('sse')

    for message in listener.listen():
        if message['type'] == 'message':
            message_decode = message['data'].decode('utf-8').replace('"', "").replace("'", '"')
            print(f"Message reçu: {message_decode}")

            # Retirer le premier et le dernier caractère du message (")
            # message_data_message = message_decode['message'].strip('"') Marche pas
            # print(f"Message reçu: {message_data_message}")

            # Essayer de corriger le formatage du JSON

            message_data = json.loads(message_decode)
            

            # Vérifier si 'Data' ou 'Sensor' est contenu dans message_data['type']
            if 'Data' in message_data['type']:
                formatted_message = message_data['message']
                send_event(message_data['type'], 'message', formatted_message)
            elif 'Sensor' in message_data['type']:
                formatted_message = message_data['message']
                send_event('Sensor', 'message', formatted_message)
