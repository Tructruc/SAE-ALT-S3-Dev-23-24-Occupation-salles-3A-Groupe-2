from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from app.models import Sensor, Data
from deepserializer import DeepViewSet
from app.serializers import ByRoomSerializer
from django.utils import timezone
from dateutil.parser import parse

from django.utils.dateparse import parse_datetime

import logging
import time

logger = logging.getLogger('API')

class ByRoomViewSet(DeepViewSet):
    """
    View uses for ByRoom endpoint using Sensor model, that permit to get all the data from 
    a room with the sort that we need on this endpoint
    """

    depth = 0
    queryset = Sensor.objects
    use_case = 'by_room_sort'

    def filter_sensor_data(self, sensor, date_from, date_to, depth, last_data=None):
        # Convertir les chaînes de date en objets datetime
        if date_from:
            date_from = parse_datetime(date_from)
        if date_to:
            date_to = parse_datetime(date_to)

        # Filtrer les données en utilisant les filtres de requête de Django
        queryset = sensor.all_data.all().order_by('time')
        if date_from:
            queryset = queryset.filter(time__gte=date_from)
        if date_to:
            queryset = queryset.filter(time__lte=date_to)
        
        if depth > 0:
            filtered_data = list(queryset)
            # Gérer spécifiquement last_data égal à 0
            if last_data is not None:
                if int(last_data) == 0:
                    sensor.filtered_data = []
                else:
                    sensor.filtered_data = filtered_data[-int(last_data):]
            else:
                sensor.filtered_data = filtered_data
            sensor.sensor = sensor
        elif depth == 0:
            # Gérer spécifiquement last_data égal à 0
            if last_data is not None:
                if int(last_data) == 0:
                    sensor.data_ids = []
                else:
                    sensor.data_ids = [data.id for data in queryset][-int(last_data):]
            else:
                sensor.data_ids = [data.id for data in queryset]
            sensor.sensor_id = sensor.deveui
        return sensor

    def get_queryset(self):
        """
        This methode is call we the endpoint for all room is called.
        Is getting all the parameters from the request and call the filter_sensor_data method for each sensor, to sort them properly.
        """
        queryset = super().get_queryset()
        params = self.request.query_params
        date_from = params.get('from')
        date_to = params.get('to')
        depth = 0 if params.get('depth') is None else int(params.get('depth'))
        last_data = params.get('last_data')

        for sensor in queryset:
            self.filter_sensor_data(sensor, date_from, date_to, depth, last_data)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        This methode is call we the endpoint for one room is called.
        Do the same things as get_queryset but for one room.
        """
        room_id = kwargs.get('pk')
        params = request.query_params
        date_from = params.get('from')
        date_to = params.get('to')
        depth = 0 if params.get('depth') is None else int(params.get('depth'))
        last_data = params.get('last_data')

        try:
            sensor = Sensor.objects.get(room=room_id)
            sensor = self.filter_sensor_data(sensor, date_from, date_to, depth, last_data)
        except Sensor.DoesNotExist:
            raise NotFound('Room does not exist')

        serializer = ByRoomSerializer(sensor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = ByRoomSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    