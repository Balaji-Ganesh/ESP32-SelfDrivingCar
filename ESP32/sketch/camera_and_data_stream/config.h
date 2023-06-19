/**
 * This file contains the configurations for the motor controls.
*/
#include <NewPing.h>

#define LIGHT_PIN 4

#define UP 1
#define DOWN 2
#define LEFT 3
#define RIGHT 4
#define STOP 0

#define RIGHT_MOTOR 0
#define LEFT_MOTOR 1

#define FORWARD 1
#define BACKWARD -1

// ultra-sonic setup..
#define TRIGGER_PIN 1    // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN 3       // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.