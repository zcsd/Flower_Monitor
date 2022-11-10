import RPi.GPIO as GPIO
import time
from datetime import datetime

from mqtt_client import MqttClient

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

my_mqtt_client = MqttClient("192.168.1.226", "mqttclient", "mqttclient", "pi101-motion")
    
try:
    while True:
        time.sleep(0.2)
        current_state = GPIO.input(4)
        if current_state == 1:
            #print("Somebody is moving.", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data = {"state": "ON"}
            my_mqtt_client.pub_msg("living_room/motion_sensor", data)
            time.sleep(7)
            current_state = 0
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
