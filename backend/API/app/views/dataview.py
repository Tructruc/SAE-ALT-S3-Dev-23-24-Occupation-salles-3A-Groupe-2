import datetime
from rest_framework import status
from rest_framework.response import Response
from deepserializer import DeepViewSet
from app.models import Data
from app.serializers import DataSerializer

from django.utils.dateparse import parse_datetime

class DataViewSet(DeepViewSet):
    """
    View used for the Data model with data endpoint with the sort that we need on this endpoint
    """
    depth = 0
    queryset = Data.objects
    use_case = 'data_date_sort'

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        date_from = params.get('from')
        date_to = params.get('to')

        if date_from:
            date_from = parse_datetime(date_from)
            queryset = queryset.filter(time__gte=date_from)

        if date_to:
            date_to = parse_datetime(date_to)
            queryset = queryset.filter(time__lte=date_to)

        return queryset.order_by('time')
