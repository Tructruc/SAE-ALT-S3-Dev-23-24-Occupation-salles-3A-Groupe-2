import pytz
import logging

from datetime import datetime
from django.test import TestCase
from app.models import Sensor, Data
from app.tests.utils import setup_logger

setup_logger()
logger = logging.getLogger("TEST")

class DepthTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        logger.info("\nSetting up data for DepthTestCase")

        timezone = pytz.timezone('Europe/Paris')
        cls.local_time = datetime.now(timezone).isoformat()

        logger.debug(f"Local time : {cls.local_time}")

        # Création d'un sensor unique pour chaque test
        cls.sensor = Sensor.objects.create(
            deveui="24e124128c019417",
            devicename="AM107-33",
            room="E103",
            building="E",
            floor=1,
            batterylevel=60.0,
            externalpowersource=False
        )

        cls.data_id = Data.objects.create(
            time=cls.local_time,
            temperature=23.5,
            humidity=45.3,
            activity=0,
            co2=500,
            tvoc=10000,
            illuminance=20000,
            infrared=30000,
            infrared_and_visible=40000,
            pressure=1013.25,
            sensor=cls.sensor
        ).id

        cls.local_time = str(cls.local_time).split('+')[0]

        logger.debug(f"Data created : {cls.data_id} at time {cls.local_time}")

    def test_endpoint_depth_0_sensor(self):
        response = self.client.get('/Sensor/?depth=0')
        logger.debug(f"Depth_0_sensor_reponse : {response.json()}")

        expected = [
            {
                "deveui": "24e124128c019417",
                "devicename": "AM107-33",
                "room": "E103",
                "building": "E",
                "floor": 1,
                "batterylevel": 60.0,
                "externalpowersource": False,
                "all_data": [self.data_id]  # Utilisez self.data_id
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_depth_0_data(self):
        response = self.client.get('/Data/?depth=0')

        logger.debug(f"Depth_0_data_reponse : {response.json()}")

        expected = [
            {
                "id": self.data_id,
                "time": self.local_time,
                "temperature": 23.5,
                "humidity": 45.3,
                "activity": 0,
                "co2": 500,
                "tvoc": 10000,
                "illuminance": 20000,
                "infrared": 30000,
                "infrared_and_visible": 40000,
                "pressure": 1013.25,
                "sensor": "24e124128c019417"
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_depth_0_byroom(self):
        reponse = self.client.get('/ByRoom/?depth=0')

        logger.debug(f"Depth_0_byroom_reponse : {reponse.json()}")

        expected = [
            {
                "room": "E103",
                "all_data": [
                    self.data_id
                ],
                "sensor": "24e124128c019417",
                "building": "E",
                "floor": 1
            }
        ]

        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.json(), expected)

    def test_endpoint_depth_1_sensor(self):
        response = self.client.get('/Sensor/?depth=1')

        logger.debug(f"Depth_1_sensor_reponse : {response.json()}")

        expected = [
            {
                "deveui": "24e124128c019417",
                "devicename": "AM107-33",
                "room": "E103",
                "building": "E",
                "floor": 1,
                "batterylevel": 60.0,
                "externalpowersource": False,
                "all_data": [
                    {
                        "id": self.data_id,
                        "time": self.local_time,
                        "temperature": 23.5,
                        "humidity": 45.3,
                        "activity": 0,
                        "co2": 500,
                        "tvoc": 10000,
                        "illuminance": 20000,
                        "infrared": 30000,
                        "infrared_and_visible": 40000,
                        "pressure": 1013.25,
                    }
                ]
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_depth_1_data(self): 
        response = self.client.get('/Data/?depth=1')

        logger.debug(f"Depth_1_data_reponse : {response.json()}")

        expected = [
            {
                "id": self.data_id,
                "time": self.local_time,
                "temperature": 23.5,
                "humidity": 45.3,
                "activity": 0,
                "co2": 500,
                "tvoc": 10000,
                "illuminance": 20000,
                "infrared": 30000,
                "infrared_and_visible": 40000,
                "pressure": 1013.25,
                "sensor": {
                    "deveui": "24e124128c019417",
                    "devicename": "AM107-33",
                    "room": "E103",
                    "building": "E",
                    "floor": 1,
                    "batterylevel": 60.0,
                    "externalpowersource": False,
                }
            } 
        ]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), expected)

    def test_endpoint_depth_1_byroom(self):
        response = self.client.get('/ByRoom/?depth=1')

        logger.debug(f"Depth_1_byroom_reponse : {response.json()}")

        expected = [
            {
                "room": "E103",
                "all_data": [
                    {
                        "id": self.data_id,
                        "time": self.local_time,
                        "temperature": 23.5,
                        "humidity": 45.3,
                        "activity": 0.0,
                        "co2": 500.0,
                        "tvoc": 10000.0,
                        "illuminance": 20000.0,
                        "infrared": 30000.0,
                        "infrared_and_visible": 40000.0,
                        "pressure": 1013.25,
                    }
                ],
                "sensor": {
                    "deveui": "24e124128c019417",
                    "devicename": "AM107-33",
                    "batterylevel": 60.0,
                    "externalpowersource": False,
                },
                "building": "E",
                "floor": 1
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

        

