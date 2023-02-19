/*
connection schematic..
  connect motors as per the labels on the sheild as below.
  !! Make sure to connect the + and - terminals of motors properly.

                FORWARD
              ^^^^^^^^^^^
              M2      M1
  RIGHT <<-   ..      ..   -->>> LEFT
              M3      M4
              \/\/\/\/\/
               BACKWARD

  with Arduino Blue control - Broxcode

*/

#include <AFMotor.h>  // library for controlling motors.

// Defining the motors to be used -- with their frequency
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);
AF_DCMotor motor3(3, MOTOR12_64KHZ);
AF_DCMotor motor4(4, MOTOR12_64KHZ);

// Helper function declarations..
void set_dir_command(uint8_t command);

// enum for choosing constants for directions..
enum {
  STOP,  // 0
  FWD,   // 1
  BWD,   // 2
  LFT,   // 3
  RGHT,  // 4
};

void setup() {
  // set the speed level of motors.
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(250);
  motor4.setSpeed(250);
  // Setup the serial communication
  Serial.begin(9600);
  Serial.println("commands: ");
  Serial.println(FWD);
  Serial.println(BWD);
  Serial.println(LFT);
  Serial.println(RGHT);
  Serial.println(STOP);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    Serial.print("Received data: ");
    Serial.println(data-49);
    set_dir_command(data-49);  // perform direction.
  } else {
    // set_dir_command(STOP);
  }
}

void set_dir_command(uint8_t command) {  // set-direction-command: {FORWARD, BACKWARD, RELEASE}
  Serial.print("Command ::::::::: ");
  // set the speed level..
  if (command != STOP) {
    motor1.setSpeed(250);
    motor1.setSpeed(250);
    motor2.setSpeed(250);
    motor3.setSpeed(250);
  } else {
    motor1.setSpeed(0);
    motor1.setSpeed(0);
    motor2.setSpeed(0);
    motor3.setSpeed(0);
  }

  // perform respective action..
  switch (command) {
    case FWD:
      {
        Serial.println("FORWARD");
        motor1.run(FORWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(FORWARD);
        break;
      }
    case BWD:
      {
        Serial.println("BACKWARD");
        motor1.run(BACKWARD);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(BACKWARD);
        break;
      }
    case LFT:
      {
        Serial.println("LEFT");
        motor1.run(BACKWARD);
        motor2.run(BACKWARD);
        motor3.run(FORWARD);
        motor4.run(FORWARD);
        break;
      }
    case RGHT:
      {
        Serial.println("RIGHT");
        motor1.run(FORWARD);
        motor2.run(FORWARD);
        motor3.run(BACKWARD);
        motor4.run(BACKWARD);
        break;
      }
    case STOP:
      {
        // no break, so, go to default
        // stop ..!!
      }
    default:
      {
        Serial.print("STOP -- ");
        Serial.println(command);
        motor1.run(RELEASE);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(RELEASE);
        break;
      }
  }
}
