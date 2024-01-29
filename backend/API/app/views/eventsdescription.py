from django.http import JsonResponse
from app.usecases.redis import redis_sender

def events_description(request):    
    redis_sender('Data', 'TEST')
    return JsonResponse({
        "endpoints": {
            "Sensor": "/Events/Sensor/",
            "Data": "/Events/Data/"
        }
    })