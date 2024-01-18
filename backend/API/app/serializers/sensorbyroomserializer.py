from app.models import Sensor
from deepserializer import DeepSerializer

class SensorByRoomSerializer(DeepSerializer):
    """
    This serializer is to serialize sensor from ByRoom endpoint
    """
    class Meta:
        model = Sensor
        fields =[
            'deveui',
            'devicename',
            'batterylevel',
            'externalpowersource'
        ]
        depth = 0
        use_case = 'sensor_by_room'