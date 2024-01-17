from django.db.models import Prefetch
# from app.serializers import DataSerializer 
from app.usecases import data_date_sort
from deepserializer import DeepSerializer
from app.models import Sensor, Data
from rest_framework import serializers
from app.serializers.databyroomserializer import DataByRoomSerializer
from app.serializers.sensorbyroomserializer import SensorByRoomSerializer

class ByRoomSerializer(DeepSerializer):
    all_data = serializers.SerializerMethodField()
    sensor = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['room', 'all_data', 'sensor', 'building', 'floor']
        depth = 0
        use_case = 'by_room_sort'

    def get_all_data(self, obj):
        if hasattr(obj, 'filtered_data'):
            return DataByRoomSerializer(obj.filtered_data, many=True).data
        elif hasattr(obj, 'data_ids'):
            return obj.data_ids
        return [data.id for data in obj.all_data.all().order_by('time')]
    
    def get_sensor(self, obj):
        if hasattr(obj, 'sensor'):
            return SensorByRoomSerializer(obj).data
        elif hasattr(obj, 'sensor_id'):
            return obj.deveui