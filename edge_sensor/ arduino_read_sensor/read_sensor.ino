#include <dht.h>
#include <Wire.h>
#include <BH1750.h>
 
#define dhtDOPin 4  // DHT22 Sensor Digital Output
#define dhtPower 5  // DHT22 Sensor Power

#define soilMoiAOPin A0 // Soil Moisture Sensor Analog Output
#define soilMoiPower 7  // Soil Moisture Sensor Power

#define relayDOPin 3 // Fan Relay Digital Output

dht DHT;
BH1750 lightMeter;

void setup() {
  Serial.begin(9600);
  // Soil Moisture Sensor
  pinMode(soilMoiPower, OUTPUT);
  digitalWrite(soilMoiPower, LOW);
  // DHT22
  pinMode(dhtPower, OUTPUT);
  digitalWrite(dhtPower, LOW);
  // Illuminance meter BH1750
  Wire.begin();
  lightMeter.configure(BH1750::ONE_TIME_HIGH_RES_MODE);
  lightMeter.begin();
  // Relay control
  pinMode(relayDOPin, OUTPUT);
  digitalWrite(relayDOPin, LOW);
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
    } else if (inputMsg == "fan_on"){
      digitalWrite(relayDOPin, HIGH);
      Serial.println("fan_on_ok");
    } else if(inputMsg == "fan_off"){
      digitalWrite(relayDOPin, LOW);
      Serial.println("fan_off_ok");
    } else{
      Serial.print("Unknown command: ");
      Serial.println(inputMsg);
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