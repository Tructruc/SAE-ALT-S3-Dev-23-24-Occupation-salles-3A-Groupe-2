from django.db.models import Prefetch
# from app.serializers import DataSerializer 
from app.usecases import data_date_sort
from deepserializer import DeepSerializer
from app.models import Sensor, Data
from rest_framework import serializers
from app.serializers.dataserializer import DataSerializer

class ByRoomSerializer(DeepSerializer):
    all_data = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ['room', 'all_data']
        depth = 0
        use_case = 'by_room_sort'

    def get_all_data(self, obj):
        # Utiliser 'filtered_data' si disponible, sinon renvoyer 'all_data' normal
        if hasattr(obj, 'filtered_data'):
            return DataSerializer(obj.filtered_data, many=True).data
        elif hasattr(obj, 'data_ids'):
            # Pour depth == 0
            return obj.data_ids
        
        return [data.id for data in obj.all_data.all()]