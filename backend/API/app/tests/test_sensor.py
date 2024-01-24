import logging

from django.test import TestCase
from app.models import Sensor
from app.tests.utils import setup_logger

setup_logger()
logger = logging.getLogger("TEST")

class SensorTestCase(TestCase):
    def setUp(self):
        self.deveui_sensor_1 = (
            Sensor.objects.create(
                deveui="24e124128c019417", 
                devicename="AM107-33", 
                room="E103", 
                building="E", 
                floor=1, 
                batterylevel=60, 
                externalpowersource=False
            )
        ).deveui

        self.deveui_sensor_2 = (
            Sensor.objects.create(
                deveui="24e124128c019416", 
                devicename="AM107-33", 
                room="E102", 
                building="E", 
                floor=1, 
                batterylevel=11.7, 
                externalpowersource=True
            )
        ).deveui
        

    def test_basic_creation_1(self):
        sensor_test = Sensor.objects.get(deveui=self.deveui_sensor_1)
        self.assertEqual(sensor_test.deveui, '24e124128c019417')
        self.assertEqual(sensor_test.devicename, 'AM107-33')
        self.assertEqual(sensor_test.room, 'E103')
        self.assertEqual(sensor_test.building, 'E')
        self.assertEqual(sensor_test.floor, 1)
        self.assertEqual(sensor_test.batterylevel, 60.0)
        self.assertEqual(sensor_test.externalpowersource, False)

    def test_basic_creation_2(self):
        sensor_test = Sensor.objects.get(deveui=self.deveui_sensor_2)
        self.assertEqual(sensor_test.deveui, '24e124128c019416')
        self.assertEqual(sensor_test.devicename, 'AM107-33')
        self.assertEqual(sensor_test.room, 'E102')
        self.assertEqual(sensor_test.building, 'E')
        self.assertEqual(sensor_test.floor, 1)
        self.assertEqual(sensor_test.batterylevel, 11.7)
        self.assertEqual(sensor_test.externalpowersource, True)

    def test_endpoint_Sensor_basic(self):
        # Get the response for the endpoint.
        response = self.client.get('/Sensor/')
    
        # Define the expected response.
        expected = [
            {
                "deveui": "24e124128c019417",
                "devicename": "AM107-33",
                "room": "E103",
                "building": "E",
                "floor": 1,
                "batterylevel": 60.0,
                "externalpowersource": False,
                "all_data" : [],
            },
            {
                "deveui": "24e124128c019416",
                "devicename": "AM107-33",
                "room": "E102",
                "building": "E",
                "floor": 1,
                "batterylevel": 11.7,
                "externalpowersource": True,
                "all_data" : [],
            }
        ]

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response is the expected one.
        self.assertEqual(response.json(), expected)

    def test_endpoint_Sensor_by_deveui_1(self):
        # Get the response for the endpoint.
        response = self.client.get(f'/Sensor/{self.deveui_sensor_1}/')

        # Define the expected response.
        excepted = {
            "deveui": "24e124128c019417",
            "devicename": "AM107-33",
            "room": "E103",
            "building": "E",
            "floor": 1,
            "batterylevel": 60.0,
            "externalpowersource": False,
            "all_data" : [],
        }

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response is the expected one.
        self.assertEqual(response.json(), excepted)

    def test_endpoint_Sensor_by_deveui_2(self):
        # Get the response for the endpoint.
        response = self.client.get(f'/Sensor/{self.deveui_sensor_2}/')

        # Define the expected response.
        excepted = {
            "deveui": "24e124128c019416",
            "devicename": "AM107-33",
            "room": "E102",
            "building": "E",
            "floor": 1,
            "batterylevel": 11.7,
            "externalpowersource": True,
            "all_data" : [],
        }

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response is the expected one.
        self.assertEqual(response.json(), excepted)
