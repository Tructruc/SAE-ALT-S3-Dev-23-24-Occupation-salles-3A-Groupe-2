"""
ASGI config for API project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django_eventstream.routing

from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = ProtocolTypeRouter({
    'http': URLRouter([
        path('Events/Sensor/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), {'format-channels': ['Sensor']}), 
        path('Events/Data/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), {'format-channels': ['Data']}),
        re_path(r'^Events/Sensor/(?P<channel_name>\w+)/$', 
                AuthMiddlewareStack(
                    URLRouter(
                        django_eventstream.routing.urlpatterns
                    )
                ), 
                {'format-channels': ['Sensor/{channel_name}']}
        ),
         re_path(r'^Events/Data/(?P<channel_name>\w+)/$', 
                AuthMiddlewareStack(
                    URLRouter(
                        django_eventstream.routing.urlpatterns
                    )
                ), 
                {'format-channels': ['Data/{channel_name}']}
        ),
        re_path(r'', get_asgi_application()),
    ]),
})