# Edge Sensor (RPi-MQTT-Serial)

## Hardware:
- Raspberry Pi 4B  <=> USB Serial Communication <=>  Arduino Uno

- GY-30 Light Intensity Sensor, connect with Arduino.

- DHT11/22 Temperature and Humidity sensor, connect with Arduino.

- HW-080 Soil Moisture Sensor, connect with Arduino.

## Deployment

```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
cd edge_sensor/rpi_mqtt_serial
pip3 install -r requirements.txt
python3 start.py
```

For product development (Autostart, kepp alive forever)
```
sudo apt install nodejs npm
sudo npm install pm2 -g
pm2 start start.py --name myserial --interpreter python3
pm2 save
sudo chattr +i /home/pi/.pm2/dump.pm2     (VERY IMPORTANT! Lock dump.p2)
sudo pm2 startup systemd -u pi --hp /home/pi
```