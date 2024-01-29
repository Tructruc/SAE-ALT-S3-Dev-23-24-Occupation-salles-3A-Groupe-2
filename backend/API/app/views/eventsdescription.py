from django.http import JsonResponse

def events_description(request):    
    return JsonResponse({
        "endpoints": {
            "Sensor": "/Events/Sensor/",
            "Data": "/Events/Data/"
        }
    })