import logging
import pytz

from datetime import datetime
from django.test import TestCase
from app.models import Sensor, Data
from app.tests.utils import setup_logger

setup_logger()
logger = logging.getLogger("TEST") 

class ByRoomSortTestCase(TestCase):
    def setUp(self):
        self.sensor_1 = Sensor.objects.create(
            deveui="24e124128c019417", 
            devicename="AM107-33", 
            room="E103", 
            building="E", 
            floor=1, 
            batterylevel=60, 
            externalpowersource=False
        )

        timezone = pytz.timezone('Europe/Paris')
        self.local_time_1 = datetime.now(timezone).isoformat()

        self.data_1 = Data.objects.create(
            time=self.local_time_1,
            temperature=23.5,
            humidity=45.3,
            activity=0,
            co2=500,
            tvoc=10000,
            illuminance=20000,
            infrared=30000,
            infrared_and_visible=40000,
            pressure=1013.25,
            sensor=Sensor.objects.get(deveui=self.sensor_1.deveui)
        )

        self.local_time_2 = datetime.now(timezone).isoformat()

        self.data_2 = Data.objects.create(
            time=self.local_time_2,
            temperature=23.5,
            humidity=45.3,
            activity=0,
            co2=500,
            tvoc=10000,
            illuminance=20000,
            infrared=30000,
            infrared_and_visible=40000,
            pressure=1013.25,
            sensor=Sensor.objects.get(deveui=self.sensor_1.deveui)
        )

        self.local_time_3 = datetime.now(timezone).isoformat()

        self.data_3 = Data.objects.create(
            time=self.local_time_3,
            temperature=23.5,
            humidity=45.3,
            activity=0,
            co2=500,
            tvoc=10000,
            illuminance=20000,
            infrared=30000,
            infrared_and_visible=40000,
            pressure=1013.25,
            sensor=Sensor.objects.get(deveui=self.sensor_1.deveui)
        )

        self.local_time_1 = str(self.local_time_1).split('+')[0]
        self.local_time_2 = str(self.local_time_2).split('+')[0]
        self.local_time_3 = str(self.local_time_3).split('+')[0]

    def test_endpoint_byroomsort_last_data_1(self):
        response = self.client.get('/ByRoom/E103/?last_data=2')

        expected = {
            "room": self.sensor_1.room,
            "all_data": [
                self.data_2.id,
                self.data_3.id
            ],
            "sensor": self.sensor_1.deveui,
            "building": self.sensor_1.building,
            "floor": self.sensor_1.floor
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


    def test_endpoint_byroomsort_last_data_2(self):
        response = self.client.get('/ByRoom/E103/?last_data=1')

        expected = {
            "room": self.sensor_1.room,
            "all_data": [
                self.data_3.id
            ],
            "sensor": self.sensor_1.deveui,
            "building": self.sensor_1.building,
            "floor": self.sensor_1.floor
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_byroomsort_from_to_1(self):
        response = self.client.get('/ByRoom/E103/?from=' + self.local_time_1 + '&to=' + self.local_time_2)

        expected = {
            "room": self.sensor_1.room,
            "all_data": [
                self.data_1.id,
                self.data_2.id
            ],
            "sensor": self.sensor_1.deveui,
            "building": self.sensor_1.building,
            "floor": self.sensor_1.floor
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

