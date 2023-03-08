/*
This script is merge of `collision_avoidance` and `./ArduinoSketches/BluetoothControl_with_L239D/ContinousStream_v0.1`

*/

#include <AFMotor.h>  // library for controlling motors.
#include <NewPing.h>

#define TRIGGER_PIN A0             // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN A1                // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200           // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define MAX_COLLISION_DISTANCE 10  // At what distance from car, going further fwd is to be stopped.

// Defining the motors to be used -- with their frequency
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);
AF_DCMotor motor3(3, MOTOR12_64KHZ);
AF_DCMotor motor4(4, MOTOR12_64KHZ);

// defining collision avoidance required pins
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);  // NewPing setup of pins and maximum distance.
int buzzerPin = A2;
int redLedPin = A3;
int greenLedPin = A4;
int collision_distance = 0;  // to perform other actions based on collision..

// Helper function declarations..
void set_dir_command(char command);

// int hornPin = A0;

void setup() {
  // set the speed level of motors.
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(250);
  motor4.setSpeed(250);
  // Setup the serial communication
  Serial.begin(9600);
  // setup the pins of collision avoidance
  pinMode(buzzerPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
}

void loop() {
  receive_control_commands();
  pingCollisionDistance();
}

/*** Motor controls ***/
void receive_control_commands() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    Serial.print("Received data: ");
    Serial.println(data);
    set_dir_command(data);  // perform direction.
  } else {                  // When received no command -- stop.
    Serial.println("[INFO] No command received: STOP state.");
    set_dir_command('S');
  }
}

void set_dir_command(char command) {  // set-direction-command: {FORWARD, BACKWARD, RELEASE}
  Serial.print("Command ::::::::: ");
  // set the speed level..
  if (command != 'S') {
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
    case 'F':
      {
        Serial.println("FORWARD");
        if (collision_distance < MAX_COLLISION_DISTANCE) {
          Serial.print("!!Warning!!: Collision ahead. Cannot go FWD, try other directions.");
        } else {
          motor1.run(FORWARD);
          motor2.run(FORWARD);
          motor3.run(FORWARD);
          motor4.run(FORWARD);
        }
        break;
      }
    case 'B':
      {
        Serial.println("BACKWARD");
        motor1.run(BACKWARD);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(BACKWARD);
        break;
      }
    case 'L':
      {
        Serial.println("LEFT");
        motor1.run(BACKWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(BACKWARD);
        break;
      }
    case 'R':
      {
        Serial.println("RIGHT");
        motor1.run(FORWARD);
        motor2.run(BACKWARD);
        motor3.run(BACKWARD);
        motor4.run(FORWARD);
        break;
      }
    // case 'V':
    //   {
    //     Serial.println('Horn ON');
    //     analogWrite(hornPin, HIGH);
    //     break;
    //   }
    // case 'v':
    //   {
    //     Serial.println('Horn OFF');
    //     analogWrite(hornPin, LOW);
    //     break;
    //   }
    case 'S':
      {
        // no break, so, go to default
        // stop ..!!
      }
    default:
      {
        Serial.print("STOP");
        Serial.println(command);
        motor1.run(RELEASE);
        motor2.run(RELEASE);
        motor3.run(RELEASE);
        motor4.run(RELEASE);
        break;
      }
  }
}

/** Collision Avoidance **/
void pingCollisionDistance() {
  delay(50);  // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  Serial.print("Ping: ");
  collision_distance = sonar.ping_cm();
  Serial.print(collision_distance);  // Send ping, get distance in cm and print result (0 = outside set distance range)
  Serial.println("cm");
  if (collision_distance <= MAX_COLLISION_DISTANCE) {  // when collision is at or less than 10cm's.
    digitalWrite(buzzerPin, HIGH);
    digitalWrite(redLedPin, HIGH);
    digitalWrite(greenLedPin, LOW);
    Serial.println("Collision is nearby");
  } else {
    digitalWrite(buzzerPin, LOW);
    digitalWrite(redLedPin, LOW);
    digitalWrite(greenLedPin, HIGH);
  }
}