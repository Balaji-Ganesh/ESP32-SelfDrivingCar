#include <NewPing.h>

#define TRIGGER_PIN  A0  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     A1  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
int buzzerPin = A2;
int redLedPin = A3;
int greenLedPin = A4;

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
  pinMode(buzzerPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
}

int distance=0;
void loop() {
  delay(50);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  Serial.print("Ping: ");
  distance = sonar.ping_cm();
  Serial.print(distance); // Send ping, get distance in cm and print result (0 = outside set distance range)
  Serial.println("cm");
  if(distance < 30){
    digitalWrite(buzzerPin, HIGH);
    digitalWrite(redLedPin, HIGH);
    digitalWrite(greenLedPin, LOW);
    Serial.println("Buzzer ON");
  }
  else{
    digitalWrite(buzzerPin, LOW);  
    digitalWrite(redLedPin, LOW);
    digitalWrite(greenLedPin, HIGH);
    Serial.println("Buzzer OFF");
  }
}
