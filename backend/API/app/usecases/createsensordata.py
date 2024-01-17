import pytz
import logging

from app.models import Sensor, Data
from deepserializer import DeepSerializer
from datetime import datetime

logger = logging.getLogger('API')

def create_sensor_data(receive_dict, topic)     :
    """
    This method is called by the MQTT listener when a message is received.
    It onnly work with the two topics defined in the MQTT listener.

    It can create a sensor or a data object depending on the topic.
    And it using to two topic to complete content of the sensor and data object together with update or create.

    receive_dict from MQTT listener example by topic:

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

    :param receive_dict: The MQTT message received.
    :param topic: The MQTT topic to listen to.
    """

    logger.debug("Let's create a sensor !")

    if topic == "application/1/device/+/event/status":
        logger.debug("Create Sensor from status message")

        serializer = DeepSerializer.get_serializer(Sensor)

        serializer_instance = serializer()

        _, representation = serializer_instance.update_or_create({
            'deveui' : receive_dict['devEUI'],
            'devicename' : receive_dict['deviceName'],
            'batterylevel' : receive_dict['batteryLevel'],
            'externalpowersource' : receive_dict['externalPowerSource']
        }, {})

        logger.debug("Sensor created !")
        logger.debug(representation)

    elif topic == "AM107/by-room/#" :
        logger.debug("Create Sensor from by-room message")

        serializer = DeepSerializer.get_serializer(Sensor)

        serializer_instance = serializer()

        pk_sensor, representation_sensor = serializer_instance.update_or_create({
            'deveui' : receive_dict[1]['devEUI'],
            'devicename' : receive_dict[1]['deviceName'],
            'room' : receive_dict[1]['room'],
            'building' : receive_dict[1]['Building'],
            **({'floor': int(receive_dict[1]['floor'])} if 'floor' in receive_dict[1] else {})
        }, {})

        serializer = DeepSerializer.get_serializer(Data)

        serializer_instance = serializer()

        sensor = {
            'deveui' : pk_sensor
        }
        
        timezone = pytz.timezone('Europe/Paris')
        local_time = datetime.now(timezone)


        pk_data = serializer_instance.deep_create({
            'time': local_time,
            'temperature' : receive_dict[0]['temperature'],
            'humidity' : receive_dict[0]['humidity'],
            'activity' : receive_dict[0]['activity'],
            'co2' : receive_dict[0]['co2'],
            'tvoc' : receive_dict[0]['tvoc'],
            'illuminance' : receive_dict[0]['illumination'],
            'infrared' : receive_dict[0]['infrared'],
            'infrared_and_visible' : receive_dict[0]['infrared_and_visible'],
            'pressure' : receive_dict[0]['pressure'],
            'sensor' : sensor
        }, {})

        logger.debug("Data and Sensor create !")
    else :
        logger.debug("Topic not recognized in createsensordata.py")