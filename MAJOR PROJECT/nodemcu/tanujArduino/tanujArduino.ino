#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHTPIN 4 //D2

const int trigPin = 2;  //D4
const int echoPin = 0;  //D3
const int Buzzer = 14; //D5
const int InfraRed = 13; //D7
const int Soil_Moisture_pin = A0; //A0
int Soil_Moisture_var;


const char* ssid     = "Aman";
const char* password = "12345678";
const char* host = "192.168.162.31";
DHT dht(DHTPIN, DHT11);


void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(Buzzer, OUTPUT); 
  digitalWrite(Buzzer, HIGH);
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(InfraRed, INPUT);
  pinMode(Soil_Moisture_pin, INPUT);
  Serial.begin(115200);
  delay(100);
  dht.begin();
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Netmask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway: ");
  Serial.println(WiFi.gatewayIP());
}
void loop() {

  float t = dht.readTemperature();
  float h = dht.readHumidity();;
  Soil_Moisture_var= analogRead(Soil_Moisture_pin);
  Soil_Moisture_var = map(Soil_Moisture_var,1000,0,0,100);
  int s=Soil_Moisture_var;
  int i=digitalRead(InfraRed);

  if(Soil_Moisture_var<30){
    digitalWrite(Buzzer,LOW);
    Serial.println("Buzzer On");
    delay(5000);
    digitalWrite(Buzzer, HIGH);
    
  }
  // digitalWrite(Buzzer, HIGH);
  long duration;
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculating the distance
  int u= duration*0.034/2;
//-----------------------------------------ultrasonic----------------------------------

  
  
  Serial.print("connecting to ");
  Serial.println(host);

  WiFiClient client;
  const int httpPort = 8000;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
 String url = "/?temp="+String(t)+"&hum="+String(h)+"&soil="+String(s)+"&ir="+String(i)+"&ultrasonic="+String(u);
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  

  Serial.println("closing connection");
  delay(5000);
}
