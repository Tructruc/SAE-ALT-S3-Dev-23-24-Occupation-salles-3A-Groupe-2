import paho.mqtt.client as mqtt
import multiprocessing
import json
import logging
import time

logger = logging.getLogger('API')

class MqttClientProcess(multiprocessing.Process):
    def __init__(self, topic):
        super().__init__()
        self.client = mqtt.Client(topic)
        self.topic = topic
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.is_running = True

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected to MQTT broker on topic: {self.topic}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            message_dict = json.loads(msg.payload.decode('utf-8'))
            logger.debug(f"Message received on {self.topic}")
            from app.usecases import create_sensor_data
            create_sensor_data(message_dict, self.topic)
        except json.JSONDecodeError:
            logger.error("Unknown error during message deserialization")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"Unexpectedly disconnected from MQTT broker (code {rc}). Attempting to reconnect... \n Topic: {self.topic}")
            self.is_running = False

    def run(self):
        logger.debug("Attempting to connect to MQTT broker")
        while True:
            if not self.is_running:
                self.reconnect()
            try:
                self.client.connect("chirpstack.iut-blagnac.fr", 1883, 60)
                self.is_running = True
                self.client.loop_start()
                while self.is_running:
                    time.sleep(10)
            except TimeoutError:
                logger.warning(f"Connection to MQTT broker timed out. Retrying in 10 seconds... \nTopic: {self.topic}")
                time.sleep(10)
            except KeyboardInterrupt:
                logger.info(f"Stopping MQTT process for topic {self.topic}")
                break
            except Exception as e:
                logger.error(f"Unknown error connecting to MQTT broker: {e}")
                time.sleep(10)
        self.client.disconnect()

    def reconnect(self):
        logger.info(f"Attempting to reconnect to MQTT broker on topic {self.topic}")
        self.client.loop_stop()
        while not self.is_running:
            try:
                self.client.reconnect()
                self.is_running = True
                self.client.loop_start()  # Redémarre la boucle de gestion des messages
                logger.info(f"Successfully reconnected to MQTT broker on topic {self.topic}")
            except TimeoutError:
                logger.warning(f"Connection to MQTT broker timed out. Retrying in 10 seconds... \nTopic: {self.topic}")
                time.sleep(10)
            except Exception as e:
                logger.error(f"Failed to reconnect to MQTT broker. Retrying in 10 seconds... Error: {e}")
                time.sleep(10)

# import paho.mqtt.client as mqtt
# import multiprocessing
# import json
# import logging
# import time

# # Configuration du logger pour suivre les activités du processus
# logger = logging.getLogger('API')

# class MqttClientProcess(multiprocessing.Process):
#     """
#     This class is used to create a process that will listen to a MQTT topic and save the data in the database.
#     """

#     def __init__(self, topic):
#         """
#         This method is used to initialize the process.

#         :param topic: The MQTT topic to listen to.
#         """
#         # Initialisation du processus avec le topic MQTT spécifié
#         super().__init__()
#         self.client = mqtt.Client()  # Création d'un client MQTT
#         self.topic = topic
#         # Configuration des callbacks pour la connexion, les messages et la déconnexion
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.on_disconnect = self.on_disconnect
#         self.is_running = True  # Flag pour contrôler la boucle principale

#     def on_connect(self, client, userdata, flags, rc):
#         """
#         This method is used to connect to the MQTT broker.

#         :param client: The MQTT client.
#         :param userdata: The MQTT user data.
#         :param flags: The MQTT flags.
#         :param rc: The MQTT return code.
#         :param topic: The MQTT topic to listen to.
#         """      
#         # Callback appelé lors de la connexion au broker MQTT
#         logger.info(f"Connected to MQTT broker on topic: {self.topic}")
#         client.subscribe(self.topic)  # Souscription au topic spécifié

#     def on_message(self, client, userdata, msg):
#         """
#         This method is when a message is received on the MQTT topic and send to the method create_sensor_data.

#         :param client: The MQTT client.
#         :param userdata: The MQTT user data.
#         :param msg: The MQTT message received.
#         :param topic: The MQTT topic to listen to.
#         """
#         # Callback appelé lors de la réception d'un message sur le topic MQTT
#         try:
#             # Décodage et traitement du message
#             message_dict = json.loads(msg.payload.decode('utf-8'))
#             logger.debug(f"Message received on {self.topic}")
#             from app.usecases import create_sensor_data
#             create_sensor_data(message_dict, self.topic)
#         except json.JSONDecodeError:
#             # Gestion des erreurs de désérialisation JSON
#             logger.error("Unknown error during message deserialization")

#     def on_disconnect(self, client, userdata, rc):
#         """
#         This method is called when the client is disconnected from the broker.

#         :param client: The MQTT client.
#         :param userdata: The MQTT user data.
#         :param rc: The disconnection return code.
#         """
#         # Callback appelé lors de la déconnexion du broker
#         if rc != 0:  # Si la déconnexion est inattendue
#             logger.warning(f"Unexpectedly disconnected from MQTT broker (code {rc}). Attempting to reconnect... \n Topic: {self.topic}")
#             self.is_running = False  # Met à jour le flag pour tenter une reconnexion

#     def run(self):
#         """
#         This method is used to start the process.
#         It will try to connect to the MQTT broker and if it fails it will wait 10 seconds before retrying.

#         If the process is stopped with a KeyboardInterrupt it will stop the process.
#         """
#         # Méthode principale du processus pour se connecter et rester connecté au broker
#         logger.debug("Attempting to connect to MQTT broker")
#         while self.is_running:
#             try:
#                 self.client.connect("chirpstack.iut-blagnac.fr", 1883, 60)
#                 self.client.loop_start()  # Démarrage de la boucle de gestion des callbacks
#                 while self.is_running:
#                     time.sleep(10)  # Pause pour éviter une utilisation excessive du CPU
#             except TimeoutError:
#                 # Gestion des erreurs de connexion
#                 logger.info(f"Connection to MQTT broker timed out. Check server address and internet connection. \nTopic: {self.topic} \nRetrying in 10 seconds.")
#                 time.sleep(10)
#             except KeyboardInterrupt:
#                 # Gestion de l'interruption par l'utilisateur
#                 logger.info(f"Stopping MQTT process for topic {self.topic}")
#                 self.is_running = False
#             except Exception as e:
#                 # Gestion des autres exceptions
#                 logger.error(f"Unknown error connecting to MQTT broker: {e}")
#                 time.sleep(10)

#         self.client.disconnect()  # Déconnexion propre du client MQTT

#     def reconnect(self):
#         # Méthode pour tenter de se reconnecter au broker
#         while not self.is_running:
#             try:
#                 self.client.reconnect()
#                 self.is_running = True
#                 logger.info(f"Reconnected to MQTT broker on topic {self.topic}")
#             except:
#                 # Gestion des échecs de reconnexion
#                 logger.error(f"Failed to reconnect to MQTT broker. Retrying in 10 seconds...")
#                 time.sleep(10)