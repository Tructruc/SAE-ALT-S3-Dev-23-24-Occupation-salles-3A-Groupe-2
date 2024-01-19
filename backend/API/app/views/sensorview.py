from deepserializer import DeepViewSet
from app.serializers import SensorSerializer
from app.models import Sensor
from rest_framework import status
from rest_framework.response import Response

class SensorViewSet(DeepViewSet):
    """
    View used for the Sensor model with sensor endpoint
    """

    depth = 0
    queryset = Sensor.objects
    use_case = 'sensor'

    def get_queryset(self):
        return super().get_queryset()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SensorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)