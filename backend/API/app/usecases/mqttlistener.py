import paho.mqtt.client as mqtt
import multiprocessing
import json
from pprint import pprint

class MqttClientProcess(multiprocessing.Process):
    def __init__(self, topic):
        super().__init__()
        self.client = mqtt.Client()
        self.topic = topic

        # Utilisez des fonctions lambda pour passer les arguments supplémentaires
        self.client.on_connect = lambda client, userdata, flags, rc: self.on_connect(client, userdata, flags, rc, self.topic)
        self.client.on_message = lambda client, userdata, msg: self.on_message(client, userdata, msg, self.topic)

    def on_connect(self, client, userdata, flags, rc, topic):
        print("Connected with result code " + str(rc) + f" to topic {topic}")
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info("Connected with result code " + str(rc) + f" to topic {topic}")
        client.subscribe(topic)

    def on_message(self, client, userdata, msg, topic):
        from app.usecases import create_sensor
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
        try:
            # Tenter de se connecter au broker MQTT
            self.client.connect("chirpstack.iut-blagnac.fr", 1883, 60)
        except TimeoutError as e:
            # Gérer l'exception TimeoutError ici
            print("La connexion a dépassé le délai imparti. Vérifiez l'adresse du serveur et votre connexion internet.")
            # Ajouter une logique de reconnexion ou terminer le programme
        except Exception as e:
            # Gérer d'autres exceptions potentielles
            print(f"Une exception a été levée: {e}")
        self.client.loop_start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Arrêt du processus.")
            self.client.disconnect()
