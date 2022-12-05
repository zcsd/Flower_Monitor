#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "DHT.h"

#define DHTTYPE DHT22
//#define DHTTYPE DHT11

#define BUILTIN_LED 2
#define MOTION_INPUT 13

uint8_t DHTPin = 15; // GPIO Number
DHT dht(DHTPin, DHTTYPE);

float temperature;
float humidity;

// WiFi
const char *ssid = "xxxxxx"; // Enter your WiFi name
const char *password = "yyyyyy";  // Enter WiFi password

// MQTT Broker
const char *mqtt_server = "192.168.1.226";
const char *mqtt_username = "mqttclient";
const char *mqtt_password = "mqttclient";

WiFiClient espClient;
PubSubClient client(espClient);

#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

long lastMsg = 0;

void setup_wifi() {
  delay(10);
  // start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    //digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    // digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    client.setKeepAlive(350);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      // client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
      digitalWrite(BUILTIN_LED, HIGH); // on 
      delay(2000);
      digitalWrite(BUILTIN_LED, LOW);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(MOTION_INPUT, INPUT);
  pinMode(BUILTIN_LED, OUTPUT); // Initialize the BUILTIN_LED pin as an output
  pinMode(DHTPin, INPUT);
  Serial.begin(115200);
  digitalWrite(BUILTIN_LED, LOW); // off led
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int motion_val = digitalRead(MOTION_INPUT);
  if (motion_val == HIGH){
     Serial.println("Motion detected.");
     client.publish("living_room/motion_sensor", "{\"state\":\"ON\"}", true);
     delay(8000);
  }

  long now = millis();
  if (now - lastMsg > 60000){
    lastMsg = now;

    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
  
    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
  
    snprintf (msg, MSG_BUFFER_SIZE, "{\"temperature\":%0.1f,\"humidity\":%0.1f}", temperature, humidity);
    Serial.print("Publish message: ");
    Serial.println(msg);
    //int length = strlen(msg);
    client.publish("living_room/env_sensor", msg, true);
    
    //digitalWrite(BUILTIN_LED, HIGH); // on 
    //delay(50);
    //digitalWrite(BUILTIN_LED, LOW);
    //delay(5000);
  }
}