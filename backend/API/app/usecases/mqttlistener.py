import paho.mqtt.client as mqtt
import multiprocessing
import json
import logging
import time

logger = logging.getLogger('API')

class MqttClientProcess(multiprocessing.Process):
    def __init__(self, topic):
        super().__init__()
        self.client = mqtt.Client()
        self.topic = topic
        self.client.on_connect = lambda client, userdata, flags, rc: self.on_connect(client, userdata, flags, rc, self.topic)
        self.client.on_message = lambda client, userdata, msg: self.on_message(client, userdata, msg, self.topic)
        self.is_running = True

    def on_connect(self, client, userdata, flags, rc, topic):        
        logger.info(f"Connexion au brocker MQTT réussie sur le topic: {topic}")
        client.subscribe(topic)

    def on_message(self, client, userdata, msg, topic):
        from app.usecases import create_sensor
        try:
            message_dict = json.loads(msg.payload.decode('utf-8'))
            logger.debug(f"Message reçus sur {topic}")
            logger.debug(message_dict)
            create_sensor(message_dict, topic)
        except json.JSONDecodeError:
            logger.error(f"Erreur inconnu lors de la désérialisation du message")

    def run(self):
        logger.debug("Tentative de connexion au brocker MQTT")
        while self.is_running:
            try:
                self.client.connect("chirpstack.iut-blagnac.fr", 1883, 60)
                self.client.loop_start()
                while self.is_running:
                    time.sleep(1)
            except TimeoutError:
                logger.info("La connexion au brocker MQTT a dépassé le délai imparti. Vérifiez l'adresse du serveur et votre connexion internet.")
                time.sleep(10) # Wait 10 seconds before retrying
            except KeyboardInterrupt:
                logger.info(f"Arrêt du processus MQTT du topic {self.topic}")
                self.is_running = False
            except Exception as e:
                logger.error(f"Erreur inconnue lors de la connexion au brocker MQTT: {e}")
                time.sleep(10)

        self.client.disconnect()
