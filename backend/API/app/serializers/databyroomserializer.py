from deepserializer import DeepSerializer
from app.models import Data

class DataByRoomSerializer(DeepSerializer):
    class Meta:
        model = Data
        fields = [
            'id', 
            'time', 
            'temperature', 
            'humidity', 
            'activity', 
            'co2', 
            'tvoc', 
            'illuminance', 
            'infrared',
            'infrared_and_visible',
            'pressure'
        ]
        depth = 0
        use_case = 'data_date_sort_by_room'