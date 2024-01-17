from app.models import Sensor
from deepserializer import DeepSerializer

class SensorSerializer(DeepSerializer):
    """
    This serializer is the default serializer for the sensor model
    """
    class Meta:
        model = Sensor
        fields = '__all__'
        depth = 0
        use_case = 'sensor'