from apscheduler.schedulers.blocking import BlockingScheduler
import Adafruit_DHT
from datetime import datetime

from mqtt_client import MqttClient

def get_dht_reading():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 14)
    if humidity is not None and temperature is not None:
        #print('Temp={0}C  Humidity={1}%'.format(temperature, humidity), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {"temperature": str(temperature), "humidity": str(humidity)}
        my_mqtt_client.pub_msg("living_room/env_sensor", data)
    else:
        print('Failed to get reading. Try again!')

if __name__ == '__main__':
    my_mqtt_client = MqttClient("192.168.1.226", "mqttclient", "mqttclient", "pi101-dht")
    
    sched = BlockingScheduler(daemon=True, timezone="Asia/Singapore")
    sched.add_job(get_dht_reading, 'interval', minutes=10, id='dht_reading', max_instances=3)
    sched.start()
    
