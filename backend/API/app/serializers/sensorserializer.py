from app.models import Sensor
from deepserializer import DeepSerializer


class SensorSerializer(DeepSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'
        depth = 1