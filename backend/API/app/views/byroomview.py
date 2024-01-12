from rest_framework import serializers, status
from rest_framework.response import Response
from app.models import Sensor, Data
from deepserializer import DeepSerializer, DeepViewSet
from django.db.models import Prefetch
from app.views import DataSerializer 
from app.usecases import data_date_sort

def test(data, date_from, date_to):
    print("cac")
    
class ByRoomSerializer(DeepSerializer):
    all_data = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['room', 'all_data']
        depth = 1

    def get_all_data(self, obj):        
        print("coucou")
        date_from = self.context.get('date_from')
        date_to = self.context.get('date_to')

        for data in obj.all_data.all():
            print(data.time)

        data_ids = obj.all_data.values_list('id', flat=True)
        all_data_qs = Data.objects.filter(id__in=data_ids)

        all_data_filtered = filter(lambda data: test(data, date_from, date_to), obj.all_data.all())
        return DataSerializer(all_data_filtered, many=True).data

# class ByRoomViewSet(DeepViewSet):
#     queryset = Sensor.objects.all()

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         params = self.request.query_params
#         date_from = params.get('from')
#         date_to = params.get('to')

#         # Appliquer la logique de tri dans Prefetch
#         data_queryset = Data.objects.all()
#         data_queryset = data_date_sort(data_queryset, date_from, date_to)

#         return queryset.prefetch_related(
#             Prefetch('all_data', queryset=data_queryset)
#         )

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = ByRoomSerializer(queryset, many=True, context={'date_from': request.query_params.get('from'), 'date_to': request.query_params.get('to')})
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ByRoomViewSet(DeepViewSet):
    queryset = Sensor.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ByRoomSerializer(queryset, many=True, context={'date_from': request.query_params.get('from'), 'date_to': request.query_params.get('to')})
        return Response(serializer.data, status=status.HTTP_200_OK)