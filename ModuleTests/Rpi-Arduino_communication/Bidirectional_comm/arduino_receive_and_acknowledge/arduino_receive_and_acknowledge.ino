void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0 ){
    String data = Serial.readStringUntil('\n');
    Serial.print("Data received: ");
    Serial.println(data); // printing becomes acknowledgement.
  }
}
