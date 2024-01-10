from django.db import models

class Sensor(models.Model) :
    
    devEUI = models.CharField(max_length=100, primary_key=True)
    deviceName = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    building = models.CharField(max_length=20)
    floor = models.IntegerField(default=0)
    batterylevel = models.FloatField(default=0.0)
    externalPowerSource = models.BooleanField(default=False)