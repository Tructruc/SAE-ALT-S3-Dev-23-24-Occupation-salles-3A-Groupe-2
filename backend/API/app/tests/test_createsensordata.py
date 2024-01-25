import logging

from django.test import TestCase
from app.models import Sensor, Data
from app.usecases import create_sensor_data
from app.tests.utils import setup_logger

setup_logger()
logger = logging.getLogger("TEST")

class CreateSensorDataTestCase(TestCase):
    """
    - application/1/device/+/event/status :
        {
            'applicationID': '1',
            'applicationName': 'AM107',
            'batteryLevel': 9.84,
            'batteryLevelUnavailable': False,
            'devEUI': '24e124128c010640',
            'deviceName': 'AM107-40',
            'externalPowerSource': False,
            'margin': 12
        }

    - AM107/by-room/# :
        [
            {
                'activity': 171,
                'co2': 997,
                'humidity': 39.5,
                'illumination': 47,
                'infrared': 8,
                'infrared_and_visible': 38,
                'pressure': 994.9,
                'temperature': 17.1,
                'tvoc': 227
            },
            {
                'Building': 'B',
                'devEUI': '24e124128c019661',
                'deviceName': 'AM107-46',
                'floor': 2,
                'room': 'Foyer-personnels'
            }
        ]
    """
    
    @classmethod
    def setUpTestData(cls):
        topic_1 = "application/1/device/+/event/status"
        topic_2 = "AM107/by-room/#"

        message_dict_topic_1_1 = {
            'applicationID': '1',
            'applicationName': 'AM107',
            'batteryLevel': 9.84,
            'batteryLevelUnavailable': False,
            'devEUI': '24e124128c010640',
            'deviceName': 'AM107-41',
            'externalPowerSource': False,
            'margin': 12
        }

        message_dict_topic_1_2 = {
            'applicationID': '1',
            'applicationName': 'AM107',
            'batteryLevel': 9.84,
            'batteryLevelUnavailable': False,
            'devEUI': '24e124128c019661',
            'deviceName': 'AM107-46',
            'externalPowerSource': False,
            'margin': 12
        }

        message_dict_topic_2_1 = [
            {
                'activity': 171,
                'co2': 997,
                'humidity': 39.5,
                'illumination': 47,
                'infrared': 8,
                'infrared_and_visible': 38,
                'pressure': 994.9,
                'temperature': 17.1,
                'tvoc': 227
            },
            {
                'Building': 'B',
                'devEUI': '24e124128c010640',
                'deviceName': 'AM107-41',
                'floor': 2,
                'room': 'Foyer-personnels'
            }
        ]


        message_dict_topic_2_2 = [
            {
                'activity': 171,
                'co2': 997,
                'humidity': 39.5,
                'illumination': 47,
                'infrared': 8,
                'infrared_and_visible': 38,
                'pressure': 994.9,
                'temperature': 17.1,
                'tvoc': 227
            },
            {
                'Building': 'B',
                'devEUI': '24e124128c019661',
                'deviceName': 'AM107-46',
                'floor': 2,
                'room': 'Foyer-personnels'
            }
        ]

        create_sensor_data(message_dict_topic_2_1, topic_2)
        create_sensor_data(message_dict_topic_2_2, topic_2)   

        create_sensor_data(message_dict_topic_1_1, topic_1)
        create_sensor_data(message_dict_topic_1_2, topic_1)
    
    def test_basics_sensor_creation_1(self):
        sensor_test = Sensor.objects.get(deveui="24e124128c010640")

        self.assertEqual(sensor_test.deveui, "24e124128c010640")
        self.assertEqual(sensor_test.devicename, "AM107-41")
        self.assertEqual(sensor_test.room, "Foyer-personnels")
        self.assertEqual(sensor_test.building, "B")
        self.assertEqual(sensor_test.floor, 2)
        self.assertEqual(sensor_test.batterylevel, 9.84)
        self.assertEqual(sensor_test.externalpowersource, False)

    def test_basics_sensor_creation_2(self):
        sensor_test = Sensor.objects.get(deveui="24e124128c019661")
        self.assertEqual(sensor_test.deveui, "24e124128c019661")
        self.assertEqual(sensor_test.devicename, "AM107-46")
        self.assertEqual(sensor_test.room, "Foyer-personnels")
        self.assertEqual(sensor_test.building, "B")
        self.assertEqual(sensor_test.floor, 2)
        self.assertEqual(sensor_test.batterylevel, 9.84)
        self.assertEqual(sensor_test.externalpowersource, False)

    def test_basics_data_creation(self):
        data_count = Data.objects.count()

        self.assertEqual(data_count, 2)

    def test_basics_data_creation_1(self):
        data_test = Data.objects.get(sensor=Sensor.objects.get(deveui="24e124128c010640"))
        self.assertEqual(data_test.temperature, 17.1)
        self.assertEqual(data_test.humidity, 39.5)
        self.assertEqual(data_test.activity, 171)
        self.assertEqual(data_test.co2, 997)
        self.assertEqual(data_test.tvoc, 227)
        self.assertEqual(data_test.illuminance, 47)
        self.assertEqual(data_test.infrared, 8)
        self.assertEqual(data_test.infrared_and_visible, 38)
        self.assertEqual(data_test.pressure, 994.9)
    
    def test_basics_data_creation_2(self):
        data_test = Data.objects.get(sensor=Sensor.objects.get(deveui="24e124128c019661"))
        self.assertEqual(data_test.temperature, 17.1)
        self.assertEqual(data_test.humidity, 39.5)
        self.assertEqual(data_test.activity, 171)
        self.assertEqual(data_test.co2, 997)
        self.assertEqual(data_test.tvoc, 227)
        self.assertEqual(data_test.illuminance, 47)
        self.assertEqual(data_test.infrared, 8)
        self.assertEqual(data_test.infrared_and_visible, 38)
        self.assertEqual(data_test.pressure, 994.9)