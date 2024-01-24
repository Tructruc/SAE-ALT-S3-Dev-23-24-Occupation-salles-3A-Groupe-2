from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from timescale.db.models.models import TimescaleModel

class Data(TimescaleModel):
    temperature = models.FloatField(default=0.0, validators=[MinValueValidator(-20), MaxValueValidator(70)])
    humidity = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    activity = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    co2 = models.FloatField(default=0.0, validators=[MinValueValidator(400), MaxValueValidator(5000)])
    tvoc = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(60000)])
    illuminance = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(60000)])
    infrared = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(60000)])
    infrared_and_visible = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(60000)])
    pressure = models.FloatField(default=0.0, validators=[MinValueValidator(300), MaxValueValidator(1100)])

    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='all_data')
