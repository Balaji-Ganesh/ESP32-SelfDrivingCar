// Initialize the traffic pins lights..
// -- of traffic light-0
int redLightPin_0 = 7;
int yellowLightPin_0 = 6;
int greenLightPin_0 = 5;
// -- of traffic light-1
int redLightPin_1 = 8;
int yellowLightPin_1 = 9;
int greenLightPin_1 = 10;

void setup() {
  Serial.begin(9600);
  // -- of traffic light-0
  pinMode(redLightPin_0, OUTPUT);
  pinMode(yellowLightPin_0, OUTPUT);
  pinMode(greenLightPin_0, OUTPUT);
  // -- of traffic light-1
  pinMode(redLightPin_1, OUTPUT);
  pinMode(yellowLightPin_1, OUTPUT);
  pinMode(greenLightPin_1, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char instruction = Serial.read();  // read the instruction from bluetooth sender
    Serial.print("Received: ");
    Serial.println(instruction);
    // act according to action..
    // if of trafficlight-0...i.e., instructions will be of capital case
    if (instruction == 'R' || instruction == 'Y' || instruction == 'G' || instruction == 'O') {
      // first turn off all lights (respectively)
      digitalWrite(redLightPin_0, LOW);
      digitalWrite(yellowLightPin_0, LOW);
      digitalWrite(greenLightPin_0, LOW);
      // then turn on respective one..
      switch (instruction) {
        case 'R':  // 'R' for "red"
          digitalWrite(redLightPin_0, HIGH);
          break;
        case 'Y':  // 'Y' for "yellow"
          digitalWrite(yellowLightPin_0, HIGH);
          break;
        case 'G':  // 'G' for "green"
          digitalWrite(greenLightPin_0, HIGH);
          break;
        case 'O':  // 'O' means OFF
          digitalWrite(redLightPin_0, LOW);
          digitalWrite(yellowLightPin_0, LOW);
          digitalWrite(greenLightPin_0, LOW);
          break;
      }
    }
    // if of trafficlight-1...i.e., instructions will be of small case
    else {
      // first turn off all lights 
      digitalWrite(redLightPin_1, LOW);
      digitalWrite(yellowLightPin_1, LOW);
      digitalWrite(greenLightPin_1, LOW);
      // then turn on respective one..
      switch (instruction) {
        case 'r':  // 'r' for "red"
          digitalWrite(redLightPin_1, HIGH);
          break;
        case 'y':  // 'y' for "yellow"
          digitalWrite(yellowLightPin_1, HIGH);
          break;
        case 'g':  // 'g' for "green"
          digitalWrite(greenLightPin_1, HIGH);
          break;
        case 'o':  // 'o' means OFF
          digitalWrite(redLightPin_1, LOW);
          digitalWrite(yellowLightPin_1, LOW);
          digitalWrite(greenLightPin_1, LOW);
          break;
      }
    }
  }
}