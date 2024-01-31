"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django_eventstream

from django.urls import include, re_path
from deepserializer import DeepViewSet
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from app.models import Data, Sensor
from django.urls import path
from app.views import DataViewSet, ByRoomViewSet, SensorViewSet, SearchViewSet, AutoCompletSearchViewSet, events_description


router = routers.DefaultRouter()
DeepViewSet.init_router(router, [
])

router.register(r'Sensor', SensorViewSet, basename='Sensor')
router.register(r'Data', DataViewSet, basename='Data')
router.register(r'ByRoom', ByRoomViewSet, basename='ByRoom')
router.register(r'Search', SearchViewSet, basename='Search')


urlpatterns = [
    path('AutoCompletSearch/', AutoCompletSearchViewSet.as_view(), name='AutoCompletSearch'),
    path('Events/', events_description, name='events_description'),
    re_path(r'', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
