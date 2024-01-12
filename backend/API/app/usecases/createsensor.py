import time
import pytz
from pprint import pprint
from app.models import Sensor, Data
from deepserializer import DeepSerializer
from datetime import datetime

def create_sensor(receive_dict, topic) :
    """
    receive_dict exmpl :

    application/1/device/+/event/status :
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

    AM107/by-room/# :
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

    pprint(receive_dict)

    print("lets create one")

    

    if topic == "application/1/device/+/event/status":
        print("--STATUS--")
        serializer = DeepSerializer.get_serializer(Sensor)

        serializer_instance = serializer()

        _, representation = serializer_instance.update_or_create({
            'deveui' : receive_dict['devEUI'],
            'devicename' : receive_dict['deviceName'],
            'batterylevel' : receive_dict['batteryLevel'],
            'externalpowersource' : receive_dict['externalPowerSource']
        }, {})

    elif topic == "AM107/by-room/#" :
        print("--BYROOM--")
        serializer = DeepSerializer.get_serializer(Sensor)

        serializer_instance = serializer()

        pk_sensor, representation_sensor = serializer_instance.update_or_create({
            'deveui' : receive_dict[1]['devEUI'],
            'devicename' : receive_dict[1]['deviceName'],
            'room' : receive_dict[1]['room'],
            'building' : receive_dict[1]['Building'],
            **({'floor': int(receive_dict[1]['floor'])} if 'floor' in receive_dict[1] else {})
        }, {})

        print("repesentation sensor : ")
        pprint(representation_sensor)

        print(f"pk : {pk_sensor}")

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

        print("repesentation data : ")
        print(pk_data)

    else :
        print("topic not recognized")
        return