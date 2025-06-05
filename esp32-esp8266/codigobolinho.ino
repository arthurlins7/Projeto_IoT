#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Warpedro1";
const char* password = "guerra123";
const char* mqtt_server = "192.168.252.22";  // e.g., "192.168.0.100"

WiFiClient espClient;
PubSubClient client(espClient);

const int ledPin = D1;
const int ldrPin = A0;
int threshold = 3;  // Quanto de luz pra acender o let -> adjust as needed

void setup_wifi() {
  Serial.begin(9600);
  Serial.println("Serial Connected");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("Wifi connected\n");

}

void reconnect() {
  while (!client.connected()) {
    client.connect("ESP8266Client");
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()){
    Serial.println("Attempting to connect to client...");
    reconnect();
  }
  else {
    Serial.println("Connected to Pi Client");
  }
  client.loop();

  int ldrValue = analogRead(ldrPin);
  String payload = String(ldrValue);
  Serial.println("Sensor reading: " + payload);
  client.publish("sensor/light", payload.c_str());

  if (ldrValue < threshold) {
    digitalWrite(ledPin, HIGH);
    client.publish("sensor/led_state", "ON");
  } else {
    digitalWrite(ledPin, 0);
    client.publish("sensor/led_state", "OFF");
  }

  delay(2000);
}