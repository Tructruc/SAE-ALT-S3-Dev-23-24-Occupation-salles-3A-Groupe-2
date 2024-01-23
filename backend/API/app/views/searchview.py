from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from app.serializers import SensorSerializer
from app.models import Sensor
from rest_framework import status
from django.db.models import Q

class SearchViewSet(ViewSet):
    """
    View used for searching Sensors by room and devicename
    """

    def list(self, request, *args, **kwargs):
        queryset = Sensor.objects.all()
        search = request.query_params.get('q', None)

        if search:
            queryset = queryset.filter(
                Q(room__icontains=search) |
                Q(devicename__icontains=search) |
                Q(deveui__icontains=search)
            )

        serializer = SensorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
