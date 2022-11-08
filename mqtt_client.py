import paho.mqtt.client as mqtt
from datetime import datetime
import json

class MqttClient:
    def __init__(self, broker, username, password):
        self.client = mqtt.Client(client_id = "pi-app")
        self.client.username_pw_set(username, password)
        self.client.connected_flag = False
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish

        self.client.connect(broker, keepalive = 60) 
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True
            print("MQTT connected successfully.", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, rc):
        self.client.connected_flag = False
        print("MQTT disconnected:", str(rc), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Trying to reconnect MQTT Broker...")
        self.client.reconnect()

    def on_publish(self, client, userdata, mid):
        print("Pub command at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def pub_command(self, data):
        self.client.publish("flower/test_sensor", payload=json.dumps(data), qos=0, retain=True)
 
    def close():
        self.client.loop_stop()
        self.client.disconnect()
