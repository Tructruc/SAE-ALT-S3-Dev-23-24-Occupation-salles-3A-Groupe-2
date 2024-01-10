from django.db import models
from timescale.db.models.models import TimescaleModel

class Data(TimescaleModel):

    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    activity = models.FloatField(default=0.0)
    co2 = models.FloatField(default=0.0)
    tvoc = models.FloatField(default=0.0)
    illuminance = models.FloatField(default=0.0)
    infrared = models.FloatField(default=0.0)
    infrared_and_visible = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)

    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
