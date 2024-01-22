import pytz
from datetime import datetime

from django.test import TestCase
from app.models import Sensor, Data

class ByRoomTestCase(TestCase):
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

        self.sensor_2 = Sensor.objects.create(
            deveui="24e124128c019416", 
            devicename="AM107-33", 
            room="E102", 
            building="E", 
            floor=1, 
            batterylevel=11.7, 
            externalpowersource=True
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
            sensor=Sensor.objects.get(deveui=self.sensor_2.deveui)
        )

        self.local_time_1 = str(self.local_time_1).split('+')[0]
        self.local_time_2 = str(self.local_time_2).split('+')[0]

    def test_endpoint_byroom(self):
        response = self.client.get('/ByRoom/')

        expected = [
            {
                "room": self.sensor_1.room,
                "all_data": [
                    self.data_1.id
                ],
                "sensor": self.sensor_1.deveui,
                "building": self.sensor_1.building,
                "floor": self.sensor_1.floor
            },
            {
                "room": self.sensor_2.room,
                "all_data": [
                    self.data_2.id
                ],
                "sensor": self.sensor_2.deveui,
                "building": self.sensor_2.building,
                "floor": self.sensor_2.floor
            }
        ]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)
    
    def test_endpoint_byroom_by_room_1(self):
        response = self.client.get(f'/ByRoom/{self.sensor_1.room}/')

        expected = {
            "room": self.sensor_1.room,
            "all_data": [
                self.data_1.id
            ],
            "sensor": self.sensor_1.deveui,
            "building": self.sensor_1.building,
            "floor": self.sensor_1.floor
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

    def test_endpoint_byroom_by_room_2(self):
        response = self.client.get(f'/ByRoom/{self.sensor_2.room}/')

        expected = {
            "room": self.sensor_2.room,
            "all_data": [
                self.data_2.id
            ],
            "sensor": self.sensor_2.deveui,
            "building": self.sensor_2.building,
            "floor": self.sensor_2.floor
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)