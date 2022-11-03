#include <dht.h>  // download the lib from https://github.com/RobTillaart/Arduino/tree/master/libraries/DHTlib
// BH1750 Illuminance meter 
#include <BH1750.h> // download the lib from https://github.com/claws/BH1750
#include <Wire.h> 
// DHT22 temperature and humidity Sensor
#define dhtDOPin 4  // Digital Output
#define dhtPower 5  // Power
// YL69 Soil Moisture Sensor
#define soilMoiAOPin A0 // Analog Output
#define soilMoiPower 7  // Power

dht DHT;
BH1750 lightMeter;

void setup() {
  Serial.begin(9600);
  // soil moisture sensor
  pinMode(soilMoiPower, OUTPUT);
  digitalWrite(soilMoiPower, LOW);
  // temperature and humidity sensor
  pinMode(dhtPower, OUTPUT);
  digitalWrite(dhtPower, LOW);
  // illuminance meter 
  lightMeter.configure(BH1750::ONE_TIME_HIGH_RES_MODE);
  lightMeter.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String inputMsg = Serial.readStringUntil('\n');
    if (inputMsg == "sm") {
      readSoilMoisture();
    } else if (inputMsg == "th"){
      readDHT();
    } else if (inputMsg == "lu"){
      readLux();
    } else {
      Serial.print("na");
      //Serial.println(inputMsg);
    }
  }
}

void readLux(){
  float lux = lightMeter.readLightLevel();
  Serial.print("lu_");
  Serial.println(lux);
}

void readDHT(){
  digitalWrite(dhtPower, HIGH);
  delay(800); 
  int readData = DHT.read22(dhtDOPin); 
  float t = DHT.temperature;
  float h = DHT.humidity;
  Serial.print("t_");
  Serial.print(t);
  Serial.print("_h_");
  Serial.println(h);
  digitalWrite(dhtPower, LOW);
}

void readSoilMoisture(){
  digitalWrite(soilMoiPower, HIGH);
  delay(50);  
  int value1 = analogRead(soilMoiAOPin);
  delay(5);
  int value2 = analogRead(soilMoiAOPin);
  int soilMoiVal = (value1 + value2) / 2;
  Serial.print("sm_");
  Serial.println(soilMoiVal);
  digitalWrite(soilMoiPower, LOW);
}