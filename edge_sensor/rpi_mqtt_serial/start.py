from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from serial_comm import SerialComm
from mqtt_client import MqttClient

def pub_message():
    temperature, humidity = my_serial.get_temperature_humidity()
    lux = my_serial.get_illuminance()

    data = {"temperature": temperature, "humidity": humidity, "lux": lux}
    my_mqtt_client.pub_env_readings(data)

def on_message(client, userdata, msg):
    # m_decode = str(msg.payload.decode("utf-8","ignore"))
    # m_in = json.loads(m_decode) #decode json data
    # m_in["sensor1"]
    print("New Message on " + msg.topic + ": " + str(msg.payload.decode("utf-8","ignore")) + " at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    my_serial = SerialComm()

    my_mqtt_client = MqttClient("192.168.1.226", "mqttclient", "mqttclient", "pi401-flower")
    my_mqtt_client.client.subscribe("flower/test_sensor")
    my_mqtt_client.client.on_message = on_message

    sched = BlockingScheduler(daemon=True, timezone="Asia/Singapore")
    sched.add_job(pub_message, 'interval', seconds=10, id='sensor_env')
    sched.start()