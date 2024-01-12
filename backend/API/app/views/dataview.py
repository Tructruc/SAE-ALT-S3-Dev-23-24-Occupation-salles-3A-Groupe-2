import datetime
from rest_framework import status
from rest_framework.response import Response
from deepserializer import DeepViewSet
from app.models import Data
from app.usecases import data_date_sort
from app.serializers import DataSerializer

class DataViewSet(DeepViewSet):
    queryset = Data.objects

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        # Convertir les paramètres de date en objets datetime conscients
        date_from = params.get('from')
        date_to = params.get('to')

        queryset = Data.objects.all().order_by('time')
        queryset_filtré = filter(lambda x: data_date_sort(x, date_from, date_to), queryset)

        return queryset_filtré

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DataSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
