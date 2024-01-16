from rest_framework import status
from rest_framework.response import Response
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
    depth = 0
    queryset = Sensor.objects
    use_case = 'by_room_sort'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     params = self.request.query_params

    #     date_from = params.get('from')
    #     date_to = params.get('to')
    #     depth_param = params.get('depth')


    #     depth = 0 if depth_param is None else int(depth_param)
    #     print("depth : ")
    #     print(depth)
    #     print("queryset : ")
    #     print(queryset)

    #     queryset = Sensor.objects.all()

    #     if depth == 0 :
    #         pass
    #     elif depth > 0 :
    #         print("depth > 0")
    #         for x in queryset:
    #             print("x : ")
    #             print(x)
    #             print("x.all_data : ")
    #             print(x.all_data)
    #             print("x.all_data.all() : ")
    #             print(x.all_data.all())
    #             x.all_data.all = filter(lambda x: data_date_sort(x, date_from, date_to), x.all_data.all())

    #     return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        date_from = params.get('from')
        print("date_from : ")
        print(date_from)
        date_to = params.get('to')
        print("date_to : ")
        print(date_to)
        depth_param = params.get('depth')
        print("depth_param : ")
        print(depth_param)

        depth = 0 if depth_param is None else int(depth_param)

        if depth > 0:
            for sensor in queryset:
                # Filtrer les données de chaque capteur
                filtered_data = list(filter(lambda data: data_date_sort(data, date_from, date_to), sensor.all_data.all()))
                print("filtered_data : ")
                print(filtered_data)
                # Stocker les données filtrées dans un attribut personnalisé
                sensor.filtered_data = filtered_data
        elif depth == 0:
            for sensor in queryset:
                # Filtrer les données de chaque capteur
                filtered_data = list(filter(lambda data: data_date_sort(data, date_from, date_to), sensor.all_data.all()))
                print("filtered_data : ")
                print(filtered_data)
                sensor.data_ids = [data.id for data in filtered_data]
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializers = ByRoomSerializer(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

# class ByRoomSerializer(DeepSerializer):
#     all_data = serializers.SerializerMethodField()

#     class Meta:
#         model = Sensor
#         fields = ['room', 'all_data']
#         depth = 0
#         use_case = 'by_room_sort'

#     def get_all_data(self, obj):        
#         print("coucou")
#         date_from = self.context.get('date_from')
#         date_to = self.context.get('date_to')

#         for data in obj.all_data.all():
#             print(data.time)

#         data_ids = obj.all_data.values_list('id', flat=True)
#         all_data_qs = Data.objects.filter(id__in=data_ids)

#         all_data_filtered = filter(lambda data: test(data, date_from, date_to), obj.all_data.all())
#         return DataSerializer(all_data_filtered, many=True).data

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

# class ByRoomViewSet(DeepViewSet):
#     depth = 0
#     queryset = Sensor.objects.all()
#     use_case = 'by_room_sort'

#     def get_queryset(self):
#         logger.debug("ici")
#         return super().get_queryset()

#     def list(self, request, *args, **kwargs):
#         logger.debug("ici")        
#         queryset = self.get_queryset()
#         serializer = ByRoomSerializer(queryset, many=True, context={'date_from': request.query_params.get('from'), 'date_to': request.query_params.get('to')})
#         return Response(serializer.data, status=status.HTTP_200_OK)