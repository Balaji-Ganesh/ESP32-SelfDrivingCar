/*
This file contains variable that are used across multiple files as a (global) variable.
idea from: https://stackoverflow.com/a/3627979
*/
#include <WebSocketsServer.h>

// for websockets..
extern WebSocketsServer camWebSocket;
extern WebSocketsServer dataTxRxWebSocket;

// for accessing of client ids.
extern uint8_t cam_num, data_num;

// for deciding: Whether to stream data over websockets or not
extern bool is_connected;

// for motor and light frequency control
extern const int PWMFreq;
extern const int PWMResolution;
extern const int PWMSpeedChannel;
extern const int PWMLightChannel;