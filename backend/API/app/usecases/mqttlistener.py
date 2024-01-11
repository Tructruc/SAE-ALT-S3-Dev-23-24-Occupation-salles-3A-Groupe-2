import paho.mqtt.client as mqtt
import threading
import json
from pprint import pprint



class MqttClientThread(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self)
        self.client = mqtt.Client()
        self.topic = topic

        # Utilisez des fonctions lambda pour passer les arguments supplémentaires
        self.client.on_connect = lambda client, userdata, flags, rc: self.on_connect(client, userdata, flags, rc, self.topic)
        self.client.on_message = lambda client, userdata, msg: self.on_message(client, userdata, msg, self.topic)

    def on_connect(self, client, userdata, flags, rc, topic):
        print("Connected with result code " + str(rc) + f" to topic {topic}")
        client.subscribe(topic)

    def on_message(self, client, userdata, msg, topic):
        from app.usecases.createsensor import create_sensor
        try:
            # Décodez le payload et convertissez-le en dictionnaire
            message_dict = json.loads(msg.payload.decode('utf-8'))
            # Affichez le message de manière formatée
            print(f"Received message on {topic}: ")
            pprint(message_dict)

            create_sensor(message_dict, topic)

        except json.JSONDecodeError:
            print(f"Error decoding JSON: {msg.payload}")

    def run(self):
        self.client.connect("chirpstack.iut-blagnac.fr", 1883, 60)
        self.client.loop_start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Arrêt du script.")
            self.client.disconnect()
