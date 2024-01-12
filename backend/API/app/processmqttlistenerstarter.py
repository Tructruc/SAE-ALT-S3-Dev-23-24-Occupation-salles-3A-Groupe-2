def start_process_mqtt_listener() :
    import logging

    from app.usecases.mqttlistener import MqttClientProcess

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Démarrage du serveur')

    mqtt_process_1 = MqttClientProcess("application/1/device/+/event/status")
    mqtt_process_1.daemon = True
    mqtt_process_1.start()
    logger.info("Process 1 started")
    print("Process 1 started")

    mqtt_process_2 = MqttClientProcess("AM107/by-room/#")
    mqtt_process_2.daemon = True
    mqtt_process_2.start()
    logger.info("Process 2 started")
    print("Process 2 started")