import json
import redis

from asgiref.sync import async_to_sync

from django_eventstream import send_event

def redis_listener(channel_name):
    # channel_layer = get_channel_layer()
    # async_to_sync(channel_layer.group_add)(channel_name, "sse")
    # try:
    #     while True:
    #         message = async_to_sync(channel_layer.receive)("sse")
    #         if message.get('type') == 'Data':
    #             print("message received")
    #             formatted_message = json.dumps(message.get('text'))
    #             send_event('Data', 'message', formatted_message)
    #         elif message.get('type') == 'Sensor':
    #             print("message received")
    #             formatted_message = json.dumps(message.get('text'))
    #             send_event('Sensor', 'message', formatted_message)
    # except :
    #     pass




    # Connect to local redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    # Subscribe to the channels
    listener = r.pubsub()
    listener.subscribe('sse')

    # Listen to the channels
    for message in listener.listen():
        print("message received")
        print(message)
        if message['type'] == 'message':
            message_decode = message['data'].decode('utf-8').replace("'", '"')
            print(message_decode)
            message_data = json.loads(message_decode)
            print(message_data)
            if message_data['type'] == 'Data':
                print("message received")
                formatted_message = json.dumps(message_data)
                send_event('Data', 'message', formatted_message)
            elif message_data['type'] == 'Sensor':
                print("message received")
                formatted_message = json.dumps(message_data)
                send_event('Sensor', 'message', formatted_message)
        