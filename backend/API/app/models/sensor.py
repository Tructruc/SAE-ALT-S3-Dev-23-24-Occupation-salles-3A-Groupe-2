from django.db import models

class Sensor(models.Model) :
    
    deveui = models.CharField(max_length=100, primary_key=True)
    devicename = models.CharField(max_length=100, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    building = models.CharField(max_length=20, blank=True, null=True)
    floor = models.IntegerField(null=True)
    batterylevel = models.FloatField( null=True)
    externalpowersource = models.BooleanField(null=True)