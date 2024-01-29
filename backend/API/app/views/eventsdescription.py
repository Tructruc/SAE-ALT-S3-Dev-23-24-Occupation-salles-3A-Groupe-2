import redis

from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def events_description(request):
    import multiprocessing
    print(multiprocessing.current_process().pid)
    print("laaaaa")

    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.publish('sse', str({'type':'Data', 'message':'Scan en cours...'}))
    return JsonResponse({
        "endpoints": {
            "Sensor": "/Events/Sensor/",
            "Data": "/Events/Data/"
        }
    })