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


*/

#include <AFMotor.h>  // library for controlling motors.
// constants for program specific
#define FWD_LEFT 101
#define FWD_RIGHT 102
#define BWD_LEFT 103
#define BWD_RIGHT 104

// Defining the motors to be used -- with their frequency
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);
AF_DCMotor motor3(3, MOTOR12_64KHZ);
AF_DCMotor motor4(4, MOTOR12_64KHZ);

// Helper function declarations..
void accelerate(unsigned long delayTime, uint8_t step = 5);
void decelerate(unsigned long delayTime, uint8_t step = 5);
void set_dir_command(uint8_t command, unsigned long);


void setup() {
  // set the speed level of motors.
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(250);
  motor4.setSpeed(250);
  // Setup the serial communication
  Serial.begin(9600);
}

void loop() {
  // Turn on the motors...
  set_dir_command(FORWARD, 5000);
  // Accelerate from zero to maximum speed..
  // accelerate(8000);

  // decelerate from max. speed to zero.
  // decelerate(8000);

  // Change the motor direction..
  set_dir_command(BACKWARD, 5000);
  // Accelerate from zero to maximum speed..
  // accelerate(8000);

  // decelerate from max. speed to zero.
  // decelerate(8000);

  set_dir_command(FWD_LEFT, 5000);
  set_dir_command(FWD_RIGHT, 5000);
  set_dir_command(BWD_LEFT, 5000);
  set_dir_command(BWD_RIGHT, 5000);

  // Stop the motors for 5 seconds.
  set_dir_command(RELEASE, 5000);
}

void set_dir_command(uint8_t command, unsigned long delayTime) {  // set-direction-command: {FORWARD, BACKWARD, RELEASE}
  Serial.print("Command for next ");
  Serial.print(delayTime / 1000);
  Serial.print(" seconds ::::::::: ");
  switch (command) {
    case FORWARD: Serial.println("FORWARD");
    case BACKWARD: Serial.println("BACKWARD");
    // !! break for above 2 is intentionally removed ...
    // reason: for above 2 and below 1 -- the same code is to be executed
    //   and `break` removal helps in acheiving that, without having repeated code.
    case RELEASE:
      {
        Serial.println("RELEASE");
        motor1.run(command);
        motor2.run(command);
        motor3.run(command);
        motor4.run(command);
        break;
      }
    case FWD_LEFT:
      {
        Serial.println("FORWARD-LEFT");
        motor1.run(FORWARD);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(FORWARD);
        break;
      }
    case FWD_RIGHT:
      {
        Serial.println("FORWARD-RIGHT");
        motor1.run(BACKWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(BACKWARD);
        break;
      }
    case BWD_LEFT:
      {
        Serial.println("BACKWARD-LEFT");
        motor1.run(FORWARD);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(BACKWARD);
        break;
      }
    case BWD_RIGHT:
      {
        Serial.println("BACKWARD-RIGHT");
        motor1.run(RELEASE);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(RELEASE);
        break;
      }
  }
  delay(delayTime);
}

void accelerate(unsigned long delayTime = 1, uint8_t step = 5) {
  Serial.println("... ACCELERATING ...");
  uint8_t i;
  for (i = 0; i < 255; i + step) {
    motor1.setSpeed(i);
    motor2.setSpeed(i);
    motor3.setSpeed(i);
    motor4.setSpeed(i);
    delay(10);  // in ms.
  }
  // after acceleration, stay at max speed for specified time.
  Serial.print("... Stays in max speed for ");
  Serial.print(delayTime);
  Serial.println(" seconds");
  delay(delayTime);  // in ms.
}

void decelerate(unsigned long delayTime = 1, uint8_t step = 5) {
  uint8_t i;
  for (i = 255; i >= 0; i - step) {
    motor1.setSpeed(i);
    motor2.setSpeed(i);
    motor3.setSpeed(i);
    motor4.setSpeed(i);
    delay(10);  // in ms.
  }
  // after deceleration, stay at min speed for specified time.
  Serial.print("... Stays in min speed for ");
  Serial.print(delayTime);
  Serial.println(" seconds");
  delay(delayTime);  // in ms.
}
