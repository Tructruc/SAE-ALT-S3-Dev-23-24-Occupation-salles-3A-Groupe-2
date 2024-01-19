import pytz
import logging

from app.models import Sensor, Data
from deepserializer import DeepSerializer
from datetime import datetime

logger = logging.getLogger('API')

# This dictionnary containe the data rande of the Sensor.
ranges = {
    'temperature': (-20, 70),
    'humidity': (0, 100),
    'activity': (0, 65535),
    'co2': (400, 5000),
    'tvoc': (0, 60000),
    'illuminance': (0, 60000),
    'infrared': (0, 60000),
    'infrared_and_visible': (0, 60000),  
    'pressure': (300, 1100)
}

def is_in_range(value, range):
    """
    This méthode is used to verify if the data of the sensor is in the right scope.
    """
    return value >= range[0] and value <= range[1]

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

    logger.debug("Let's create something !")

    logger.debug("receive_dict")
    logger.debug(receive_dict)

    if topic == "application/1/device/+/event/status":
        logger.info("Message receive on topic 'application/1/device/+/event/status'")
        try :
            logger.debug("Create Sensor from status message")

            sensor = Sensor.objects.get(deveui=receive_dict['devEUI'])

            serializer = DeepSerializer.get_serializer(Sensor)

            serializer_instance = serializer()

            _, representation = serializer_instance.update_or_create({
                'deveui' : receive_dict['devEUI'],
                'devicename' : receive_dict['deviceName'],
                **({'batterylevel' : receive_dict['batteryLevel']} if 'batteryLevel' in receive_dict else {}),
                **({'externalpowersource' : receive_dict['externalPowerSource']} if 'externalPowerSource' in receive_dict else {})
            }, {})

            logger.debug("Sensor created !")
            logger.debug(representation)
        except Sensor.DoesNotExist:
            logger.debug("Sensor does not exist, we will not update or create it to avoid conflicts or creation of Sensr that does")

    elif topic == "AM107/by-room/#" :
        logger.info("Message receive on topic 'AM107/by-room/#'")
        logger.debug("Create Sensor from by-room message")

        serializer = DeepSerializer.get_serializer(Sensor)

        serializer_instance = serializer()

        logger.debug("create the sensor from the byroom message")
        pk_sensor, representation_sensor = serializer_instance.update_or_create({
            'deveui' : receive_dict[1]['devEUI'],
            'devicename' : receive_dict[1]['deviceName'],
            **({'room': receive_dict[1]['room']} if 'room' in receive_dict[1] else {}),
            **({'building': receive_dict[1]['Building']} if 'Building' in receive_dict[1] else {}),
            **({'floor': int(receive_dict[1]['floor'])} if 'floor' in receive_dict[1] else {})
        }, {})
        logger.debug("sensor as been create from byroom")

        serializer = DeepSerializer.get_serializer(Data)

        serializer_instance = serializer()

        sensor = {'deveui': pk_sensor}
        timezone = pytz.timezone('Europe/Paris')
        local_time = datetime.now(timezone)

        required_fields = [
            'temperature', 'humidity', 'activity', 'co2', 'tvoc', 'illumination',
            'infrared', 'infrared_and_visible', 'pressure'
        ]

        print("let's check")
        if all(key in receive_dict and is_in_range(receive_dict[key], ranges[key]) for key in ranges):
            print("all fields are here")
            pk_data = serializer_instance.deep_create({
                'time': local_time,
                'temperature': receive_dict[0]['temperature'],
                'humidity': receive_dict[0]['humidity'],
                'activity': receive_dict[0]['activity'],
                'co2': receive_dict[0]['co2'],
                'tvoc': receive_dict[0]['tvoc'],
                'illuminance': receive_dict[0]['illumination'],
                'infrared': receive_dict[0]['infrared'],
                'infrared_and_visible': receive_dict[0]['infrared_and_visible'],
                'pressure': receive_dict[0]['pressure'],
                'sensor': sensor
            }, {})
            logger.debug("data as been create from byroom")
        else:
            logger.error(f"le capteur {pk_sensor} n'a pas envoyé tous les champs nécessaires ou à envoyé des valeurs erronées, onjet data non créé")

        logger.debug("Data and Sensor create !")
    else :
        logger.debug("Topic not recognized in createsensordata.py")