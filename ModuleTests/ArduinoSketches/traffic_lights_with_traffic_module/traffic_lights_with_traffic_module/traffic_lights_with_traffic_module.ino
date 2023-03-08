// Initialize the traffic pins lights..
int redLightPin = 7;
int yellowLightPin = 6;
int greenLightPin= 5;

void setup() {
  pinMode(redLightPin, OUTPUT);
  pinMode(yellowLightPin, OUTPUT);
  pinMode(greenLightPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(redLightPin, HIGH);
  delay(2000);
  digitalWrite(redLightPin, LOW);

  digitalWrite(yellowLightPin, HIGH);
  delay(2000);
  digitalWrite(yellowLightPin, LOW);

  digitalWrite(greenLightPin, HIGH);
  delay(2000);
  digitalWrite(greenLightPin, LOW);
}
