import logging
import pytz
from datetime import datetime

from django.test import TestCase
from django.utils.timezone import localtime
from app.models import Sensor, Data
from app.tests.utils import setup_logger

logger = logging.getLogger("TEST")


class DataTestCase(TestCase):
    def setUp(self):
        timezone = pytz.timezone('Europe/Paris')
        self.local_time_data_1 = datetime.now(timezone).isoformat()

        Sensor.objects.create(
            deveui="24e124128c019417", 
            devicename="AM107-33", 
            room="E103",
            building="E", 
            floor=1, 
            batterylevel=60, 
            externalpowersource=False
        )

        self.id_data_1 = (
            Data.objects.create(
                time=self.local_time_data_1, 
                temperature=23.5, 
                humidity=45.3, 
                activity=0, 
                co2=500, 
                tvoc=10000, 
                illuminance=20000, 
                infrared=30000, 
                infrared_and_visible=40000, 
                pressure=1013.25, 
                sensor=Sensor.objects.get(deveui="24e124128c019417")
            )
        ).id

        self.local_time_data_2 = datetime.now(timezone).isoformat()

        self.id_data_2 = (
            Data.objects.create(
                time=self.local_time_data_2, 
                temperature=30.5, 
                humidity=60.3, 
                activity=100, 
                co2=501, 
                tvoc=30000, 
                illuminance=20099, 
                infrared=50000, 
                infrared_and_visible=41000, 
                pressure=1015.25, 
                sensor=Sensor.objects.get(deveui="24e124128c019417")
            )
        ).id

    def test_basic_creation_1(self):
        data_test = Data.objects.get(id=self.id_data_1)

        self.assertEqual(data_test.time.isoformat(), str(self.local_time_data_1).split('+')[0])
        self.assertEqual(data_test.temperature, 23.5)
        self.assertEqual(data_test.humidity, 45.3)
        self.assertEqual(data_test.activity, 0)
        self.assertEqual(data_test.co2, 500)
        self.assertEqual(data_test.tvoc, 10000)
        self.assertEqual(data_test.illuminance, 20000)
        self.assertEqual(data_test.infrared, 30000)
        self.assertEqual(data_test.infrared_and_visible, 40000)
        self.assertEqual(data_test.pressure, 1013.25)
        self.assertEqual(data_test.sensor, Sensor.objects.get(deveui="24e124128c019417"))



    def test_basic_creation_2(self):
        data_test = Data.objects.get(id=self.id_data_2)

        self.assertEqual(data_test.time.isoformat(), str(self.local_time_data_2).split('+')[0])
        self.assertEqual(data_test.temperature, 30.5)
        self.assertEqual(data_test.humidity, 60.3)
        self.assertEqual(data_test.activity, 100)
        self.assertEqual(data_test.co2, 501)
        self.assertEqual(data_test.tvoc, 30000)
        self.assertEqual(data_test.illuminance, 20099)
        self.assertEqual(data_test.infrared, 50000)
        self.assertEqual(data_test.infrared_and_visible, 41000)
        self.assertEqual(data_test.pressure, 1015.25)
        self.assertEqual(data_test.sensor, Sensor.objects.get(deveui="24e124128c019417"))

    def test_endpoint_Data_basic(self):
        response = self.client.get('/Data/')

        expected = [
            {
                "id": self.id_data_1,
                "time": str(self.local_time_data_1).split('+')[0],
                "temperature": 23.5,
                "humidity": 45.3,
                "activity": 0.0,
                "co2": 500.0,
                "tvoc": 10000.0,
                "illuminance": 20000.0,
                "infrared": 30000.0,
                "infrared_and_visible": 40000.0,
                "pressure": 1013.25,
                "sensor": "24e124128c019417"
            },
            {
                "id": self.id_data_2,
                "time": str(self.local_time_data_2).split('+')[0],
                "temperature": 30.5,
                "humidity": 60.3,
                "activity": 100.0,
                "co2": 501.0,
                "tvoc": 30000.0,
                "illuminance": 20099.0,
                "infrared": 50000.0,
                "infrared_and_visible": 41000.0,
                "pressure": 1015.25,
                "sensor": "24e124128c019417"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_Data_by_id_1(self):
        response = self.client.get(f'/Data/{self.id_data_1}/')

        expected = {
            "id": self.id_data_1,
            "time": str(self.local_time_data_1).split('+')[0],
            "temperature": 23.5,
            "humidity": 45.3,
            "activity": 0.0,
            "co2": 500.0,
            "tvoc": 10000.0,
            "illuminance": 20000.0,
            "infrared": 30000.0,
            "infrared_and_visible": 40000.0,
            "pressure": 1013.25,
            "sensor": "24e124128c019417"
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_Data_by_id_2(self):
        response = self.client.get(f'/Data/{self.id_data_2}/')

        expected = {
            "id": self.id_data_2,
            "time": str(self.local_time_data_2).split('+')[0],
            "temperature": 30.5,
            "humidity": 60.3,
            "activity": 100.0,
            "co2": 501.0,
            "tvoc": 30000.0,
            "illuminance": 20099.0,
            "infrared": 50000.0,
            "infrared_and_visible": 41000.0,
            "pressure": 1015.25,
            "sensor": "24e124128c019417"
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)