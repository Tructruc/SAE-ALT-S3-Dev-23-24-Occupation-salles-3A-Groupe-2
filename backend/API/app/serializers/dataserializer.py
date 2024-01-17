from deepserializer import DeepSerializer
from app.models import Data

class DataSerializer(DeepSerializer):
    """
    The default serializer for the Data model
    """
    class Meta:
        model = Data
        fields = '__all__'
        depth = 0
        use_case = 'data_date_sort'