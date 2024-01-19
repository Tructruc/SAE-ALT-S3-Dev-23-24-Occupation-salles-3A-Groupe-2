from django.test import TestCase
from app.models import Sensor


class SensorTestCase(TestCase):
    def setUp(self):
        Sensor.objects.create(deveui="24e124128c019417", devicename="AM107-33", room="E103", building="E", floor=1, batterylevel=60, externalpowersource=False)
        Sensor.objects.create(deveui="24e124128c019416", devicename="AM107-33", room="E102", building="E", floor=1, batterylevel=11.7, externalpowersource=True)

    def test_basic_creation_2(self):
        sensorTest = Sensor.objects.get(deveui="24e124128c019417")
        self.assertEqual(sensorTest.deveui, '24e124128c019417')
        self.assertEqual(sensorTest.devicename, 'AM107-33')
        self.assertEqual(sensorTest.room, 'E103')
        self.assertEqual(sensorTest.building, 'E')
        self.assertEqual(sensorTest.floor, 1)
        self.assertEqual(sensorTest.batterylevel, 60)
        self.assertEqual(sensorTest.externalpowersource, False)

    def test_basic_creation_2(self):
        sensorTest = Sensor.objects.get(deveui="24e124128c019416")
        self.assertEqual(sensorTest.deveui, '24e124128c019416')
        self.assertEqual(sensorTest.devicename, 'AM107-33')
        self.assertEqual(sensorTest.room, 'E102')
        self.assertEqual(sensorTest.building, 'E')
        self.assertEqual(sensorTest.floor, 1)
        self.assertEqual(sensorTest.batterylevel, 11.7)
        self.assertEqual(sensorTest.externalpowersource, True)

    def test_endpoint_Sensor_basic(self):
        response = self.client.get('/Sensor/')
        self.assertEqual(response.status_code, 200)