from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import json

from serial_comm import SerialComm
from mqtt_client import MqttClient

def pub_message():
    temperature, humidity = my_serial.get_temperature_humidity()
    lux = my_serial.get_illuminance()

    data = {"temperature": temperature, "humidity": humidity, "lux": lux}
    my_mqtt_client.pub_env_readings(data)

def on_message(client, userdata, msg):
    #m_in = json.loads(m_decode) #decode json data
    #command = m_in["state"]
    print("New Message on " + msg.topic + ": " + str(msg.payload.decode("utf-8","ignore")) + " at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    command = str(msg.payload.decode("utf-8","ignore"))
    if msg.topic == "flower/fan_switch":
        if command == "ON":
            my_serial.turn_on_relay();
        elif command == "OFF":
            my_serial.turn_off_relay();

if __name__ == '__main__':
    my_serial = SerialComm()

    my_mqtt_client = MqttClient("192.168.1.226", "mqttclient", "mqttclient", "pi401-flower")
    my_mqtt_client.client.subscribe("flower/fan_switch")
    my_mqtt_client.client.on_message = on_message

    sched = BlockingScheduler(daemon=True, timezone="Asia/Singapore")
    sched.add_job(pub_message, 'interval', minutes=10, id='sensor_env')
    sched.start()