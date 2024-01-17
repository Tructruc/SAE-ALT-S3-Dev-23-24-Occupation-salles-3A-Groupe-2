from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import NotFound
from app.models import Sensor, Data
from deepserializer import DeepViewSet
from app.serializers import ByRoomSerializer
from app.usecases import data_date_sort
from django.utils import timezone
from dateutil.parser import parse

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
            if depth > 0:
                filtered_data = list(filter(lambda data: data_date_sort(data, date_from, date_to), sensor.all_data.all().order_by('time')))
                sensor.filtered_data = filtered_data
                sensor.sensor = sensor
                 # Last data define how many last data objects we want to return
                if last_data:
                    sensor.filtered_data = filtered_data[-int(last_data):]
            elif depth == 0:
                filtered_data = list(filter(lambda data: data_date_sort(data, date_from, date_to), sensor.all_data.all().order_by('time')))
                sensor.data_ids = [data.id for data in filtered_data]
                sensor.sensor_id = sensor.deveui
                # Last data define how many last data objects we want to return
                if last_data:
                    sensor.data_ids = sensor.data_ids[-int(last_data):]
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
    