import pytz
import logging

from django.test import TestCase
from app.models import Sensor, Data
from app.tests.utils import setup_logger
from datetime import datetime

setup_logger()
logger = logging.getLogger("TEST") 

class DataSortTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data_save_times = []
        cls.data_save_ids = []
        timezone = pytz.timezone('Europe/Paris')
        
        cls.sensor_test = Sensor.objects.create(
            deveui="24e124128c019417",
            devicename="AM107-33",
            room="E103",
            building="E",
            floor=1,
            batterylevel=60.0,
            externalpowersource=False
        )
        
        #Boucle i de 1 à 10
        for i in range(1, 10):
            current_local_time = datetime.now(timezone).isoformat()

            current_data =  (
                Data.objects.create(
                    time=current_local_time,
                    temperature=23.5,
                    humidity=45.3,
                    activity=0,
                    co2=500,
                    tvoc=10000,
                    illuminance=20000,
                    infrared=30000,
                    infrared_and_visible=40000,
                    pressure=1013.25,
                    sensor=cls.sensor_test
                )
            )

            if i == 3 or i == 4:

                cls.data_save_times.append(current_local_time)
                cls.data_save_ids.append(current_data.id)

    def test_endpoint_datasort(self):
        response = self.client.get('/Data/?from=' + self.data_save_times[0] + '&to=' + self.data_save_times[1])

        expected = [
            {
                "id": self.data_save_ids[0],
                "time": self.data_save_times[0].split('+')[0],
                "temperature": 23.5,
                "humidity": 45.3,
                "activity": 0,
                "co2": 500,
                "tvoc": 10000,
                "illuminance": 20000,
                "infrared": 30000,
                "infrared_and_visible": 40000,
                "pressure": 1013.25,
                "sensor": self.sensor_test.deveui
            },
            {
                "id": self.data_save_ids[1],
                "time": self.data_save_times[1].split('+')[0],
                "temperature": 23.5,
                "humidity": 45.3,
                "activity": 0,
                "co2": 500,
                "tvoc": 10000,
                "illuminance": 20000,
                "infrared": 30000,
                "infrared_and_visible": 40000,
                "pressure": 1013.25,
                "sensor": self.sensor_test.deveui
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


