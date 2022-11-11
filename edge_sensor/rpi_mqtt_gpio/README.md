# Edge Sensor (RPi-MQTT-GPIO)

## Hardware:
- Raspberry Pi 1, 26 Pin GPIO

- HC-SR501 Motion Sensor (+5V power), signal input on RPi GPIO 4.

- DHT11/22 Sensor(+5V power), Data input on Rpi GPIO 14.

## Deployment

```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
cd edge_sensor/rpi_mqtt_gpio
pip3 install -r requirements.txt
python3 dht_sensor.py
python3 motion_sensor.py
```

For product development (Autostart, kepp alive forever)
```
sudo apt install nodejs npm
sudo npm install pm2 -g
pm2 start dht_sensor.py --name dht --interpreter python3
pm2 start motion_sensor.py --name motion --interpreter python3
pm2 save
sudo chattr +i /home/pi/.pm2/dump.pm2     (VERY IMPORTANT! Lock dump.p2)
sudo pm2 startup systemd -u pi --hp /home/pi
```