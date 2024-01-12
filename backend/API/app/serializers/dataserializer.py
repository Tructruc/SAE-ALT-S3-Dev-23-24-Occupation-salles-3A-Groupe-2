from deepserializer import DeepSerializer
from app.models import Data

class DataSerializer(DeepSerializer):
    class Meta:
        model = Data
        fields = '__all__'
        depth = 0
        use_case = 'data_date_sort'