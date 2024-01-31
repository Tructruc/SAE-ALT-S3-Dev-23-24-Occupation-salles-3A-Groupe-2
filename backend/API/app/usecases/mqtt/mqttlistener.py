import paho.mqtt.client as mqtt
import multiprocessing
import json
import logging
import time
import uuid

logger = logging.getLogger('API')

class MqttClientProcess(multiprocessing.Process):
    def __init__(self, topic):
        super().__init__()
        # Create a cleint wiht a unique ID by concate topic and uuid
        self.client = mqtt.Client(topic + str(uuid.uuid4()))
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

    def stop(self):
        self.is_running = False
        self.client.disconnect()
        self.terminate()
