/*This script is modification of
    1. `Motors_run_and_collision_avoidance.in` (in `experiments` branch)
            - with a change that -- instead of L239D motor driver, using L298N motor driver.
            - taking controlling with bluetooth and collision avoidance
    2. `driver.cpp` of `eesp32_model` branch.
            - taking the operation motors using L298N.

  on 27th June, 2023 - Tuesday.
*/

#include <NewPing.h>

// constants for Motor controls - via L298N
#define UP 1
#define DOWN 2
#define LEFT 3
#define RIGHT 4
#define STOP 0

#define RIGHT_MOTOR 0
#define LEFT_MOTOR 1
#define NUM_MOTORS 2              // #motors attached to the car
#define TURNING_SPEED_REDUCER 0.8 // by what constant, turning speed has to be lowered on normal speed (of FWD/BWD).

#define FORWARD 1
#define BACKWARD -1

#define TRIGGER_PIN A0            // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN A1               // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 220          // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define MAX_COLLISION_DISTANCE 20 // At what distance from car, going further fwd is to be stopped.

// setup for motor controls
struct MOTOR_PINS
{
  int pinEn;
  int pinIN1;
  int pinIN2;
};

struct MOTOR_PINS motorPins[NUM_MOTORS] = {
    {5, 6, 7}, // RIGHT_MOTOR Pins (EnB, IN3, IN4)
    {3, 2, 4}, // LEFT_MOTOR  Pins (EnA, IN1, IN2)
};

// defining collision avoidance required pins
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
int buzzerPin = A2;
int redLedPin = A3;
int greenLedPin = A4;
int collision_distance = 0; // to perform other actions based on collision..

// a global variable to store the navigation received.
int navigation = STOP;      // default: STOP state.
String tempStrSpeed = "";   // default: empty
int speed = 0;              // default: 0
bool inTurnMode = false;    // whether turning LEFT or RIGHT. To lower the speed while turning. Default: No
int stateBeforeTurn = STOP; // to store the state of navigation, before making turn. For setting back to previous state after making turn.

// Utitility functions for controlling the motors...................................................
/**
 * This function will be a helper for moveCar(int). This helps in low-level control for issuing appropriate signal based on command received.
 *
 * @param motorNumber whether LEFT or RIGHT motor.
 * @param motorDirection whether in FWD way or BWD way.
 * @return nothing
 */
void rotateMotor(int motorNumber, int motorDirection)
{
  // Serial.print("rotation: ");
  // Serial.println(motorDirection);
  if (motorDirection == FORWARD)
  {
    digitalWrite(motorPins[motorNumber].pinIN1, HIGH);
    digitalWrite(motorPins[motorNumber].pinIN2, LOW);
  }
  else if (motorDirection == BACKWARD)
  {
    digitalWrite(motorPins[motorNumber].pinIN1, LOW);
    digitalWrite(motorPins[motorNumber].pinIN2, HIGH);
  }
  else
  {
    digitalWrite(motorPins[motorNumber].pinIN1, LOW);
    digitalWrite(motorPins[motorNumber].pinIN2, LOW);
  }
}

/**
 * Moves the car as per the navigation set.
 *
 *
 *
 * @param inputValue: Integer command as per `config.h`
 * @return nothing.
 */
void moveCar()
{
  // Serial.print("[MoveCar] Got value as : ");
  // Serial.println(inputValue);
  Serial.print("Nav: ");
  Serial.print(navigation);
  Serial.print(" .... ");
  Serial.print("Speed: ");
  Serial.print(speed);
  Serial.print(" .... ");

  // Set the appropriate speed as per the navigation.
  // i.e., If FWD or BWD - speed as set. otherwise (LFT or RGT) `speed`*TURNING_SPEED_REDUCER
  if (inTurnMode)
  {
    int tempSpeed = speed * TURNING_SPEED_REDUCER; // lower the speed for turning.
    analogWrite(motorPins[0].pinEn, tempSpeed);
    analogWrite(motorPins[1].pinEn, tempSpeed);
  }
  else
  {
    analogWrite(motorPins[0].pinEn, speed);
    analogWrite(motorPins[1].pinEn, speed);
  }

  // perform the navigation..
  switch (navigation)
  {
  case UP:
    if (collision_distance >= MAX_COLLISION_DISTANCE)
    {
      rotateMotor(RIGHT_MOTOR, FORWARD);
      rotateMotor(LEFT_MOTOR, FORWARD);
    }
    else
    {
      Serial.println("!!Warning!!: Collision ahead. Cannot go FWD, try other directions.");
      rotateMotor(RIGHT_MOTOR, STOP);
      rotateMotor(LEFT_MOTOR, STOP);
    }
    break;

  case DOWN:
    rotateMotor(RIGHT_MOTOR, BACKWARD);
    rotateMotor(LEFT_MOTOR, BACKWARD);
    break;

  case LEFT:
    rotateMotor(RIGHT_MOTOR, FORWARD);
    rotateMotor(LEFT_MOTOR, BACKWARD);
    break;

  case RIGHT:
    rotateMotor(RIGHT_MOTOR, BACKWARD);
    rotateMotor(LEFT_MOTOR, FORWARD);
    break;

  case STOP:
    rotateMotor(RIGHT_MOTOR, STOP);
    rotateMotor(LEFT_MOTOR, STOP);
    break;

  default:
    rotateMotor(RIGHT_MOTOR, STOP);
    rotateMotor(LEFT_MOTOR, STOP);
    break;
  }
}

/*** Motor controls ***/
void receive_control_commands()
{
  if (Serial.available() > 0)
  {
    char data = Serial.read();
    Serial.print("[INFO] Received data: ");
    Serial.println(data);

    if (isDigit(data))
    { // check is it speed or navigation
      tempStrSpeed += (char)data;
    }
    else
    {
      // set the speed of the motors.
      if (tempStrSpeed != "")
      { // if speed has set to update..
        Serial.print("Speed setting to : ");
        Serial.println(tempStrSpeed);
        speed = tempStrSpeed.toInt();
        tempStrSpeed = ""; // set back to empty, after speed has changed.
      }
      set_dir_command(data); // perform direction.
    }
  }
  // else
  // { // When received no command -- stop.
  //   // Serial.println("[INFO] No command received: STOP state.");
  //   if(navigation != STOP)  // Set to STOP, if not in STOP state.
  //     set_dir_command('S');
  // }
}

void set_dir_command(char command)
{ // set-direction-command: {FORWARD, BACKWARD, RELEASE}
  Serial.print("Command ::::::::: ");
  // set the speed level..
  // f
  //
  //
  // Find way to adjust the speed with Arduino and L298N -- gues it would be via PWM.
  //
  //
  //
  // if (command == 'F' || command == 'B')
  // {
  //   motor1.setSpeed(180);
  //   motor1.setSpeed(180);
  //   motor2.setSpeed(180);
  //   motor3.setSpeed(180);
  // }
  // else if (command == 'L' || command == 'R')
  // {
  //   motor1.setSpeed(250);
  //   motor1.setSpeed(250);
  //   motor2.setSpeed(250);
  //   motor3.setSpeed(250);
  // }
  // else
  // {
  //   motor1.setSpeed(0);
  //   motor1.setSpeed(0);
  //   motor2.setSpeed(0);
  //   motor3.setSpeed(0);
  // }

  // perform respective action..
  switch (command)
  {
  case 'F':
  {
    Serial.println("FORWARD");
    navigation = UP;
    inTurnMode = false;
    break;
  }
  case 'B':
  {
    Serial.println("BACKWARD");
    navigation = DOWN;
    inTurnMode = false;
    break;
  }
  case 'L':
  {
    Serial.println("LEFT");
    // Implementing the toggling system for turning.
    // on first command of LEFT, store the current navigation before setting left.
    if (navigation != LEFT && navigation != RIGHT)
    {
      stateBeforeTurn = navigation;
      navigation = LEFT;
      inTurnMode = true;
    }
    // upon second command of LEFT, set back to previous state.
    else
    {
      navigation = stateBeforeTurn;
      inTurnMode = false;
    }

    break;
  }
  case 'R':
  {
    Serial.println("RIGHT");
    // Implementing the toggling system for turning.
    // on first command of RIGHT, store the current navigation before setting right.
    if (navigation != LEFT && navigation != RIGHT)
    {
      stateBeforeTurn = navigation;
      navigation = RIGHT;
      inTurnMode = true;
    }
    // upon second command of RIGHT, set back to previous state.
    else
    {
      navigation = stateBeforeTurn;
      inTurnMode = false;
    }
    break;
  }
  case 'S':
  {
    Serial.println("STOP");
    navigation = STOP;
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
    // default:
    // {
    //   Serial.print("STOP.................................................................................................................!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
    //   navigation = STOP;
    //   break;
    // }
  }
}

/** Collision Avoidance **/
void pingCollisionDistance()
{
  delay(50); // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  Serial.print("Ping: ");
  collision_distance = sonar.ping_cm();
  Serial.print(collision_distance); // Send ping, get distance in cm and print result (0 = outside set distance range)
  Serial.println("cm");
  if (collision_distance <= MAX_COLLISION_DISTANCE)
  { // when collision is at or less than 10cm's.
    digitalWrite(buzzerPin, HIGH);
    digitalWrite(redLedPin, HIGH);
    digitalWrite(greenLedPin, LOW);
    Serial.println("Collision is nearby");
  }
  else
  {
    digitalWrite(buzzerPin, LOW);
    digitalWrite(redLedPin, LOW);
    digitalWrite(greenLedPin, HIGH);
  }
}

// Arduino Functions...
void setup()
{
  // Setup the serial communication
  Serial.begin(9600);

  // set the speed level of motors.
  for (int i = 0; i < NUM_MOTORS; i++)
  {
    pinMode(motorPins[i].pinEn, OUTPUT);
    pinMode(motorPins[i].pinIN1, OUTPUT);
    pinMode(motorPins[i].pinIN2, OUTPUT);
  }
  navigation = STOP; // by default set to STOP state.

  // setup the pins of collision avoidance
  pinMode(buzzerPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
}

void loop()
{
  receive_control_commands();
  pingCollisionDistance();
  moveCar(); // keep the car move in the configured navigation.
}