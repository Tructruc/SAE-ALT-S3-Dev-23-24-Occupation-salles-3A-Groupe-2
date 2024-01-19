def start_process_mqtt_listener() :
    import logging

    from app.usecases.mqttlistener import MqttClientProcess

    logger = logging.getLogger('API')

    topic_1 = "application/1/device/+/event/status"
    mqtt_process_1 = MqttClientProcess(topic_1)
    mqtt_process_1.daemon = True
    mqtt_process_1.start()
    logger.info("MQQT listener process on topic 1 started")

    topic_2 = "AM107/by-room/#"
    mqtt_process_2 = MqttClientProcess(topic_2)
    mqtt_process_2.daemon = True
    mqtt_process_2.start()
    logger.info("MQQT listener process on topic 2 started")