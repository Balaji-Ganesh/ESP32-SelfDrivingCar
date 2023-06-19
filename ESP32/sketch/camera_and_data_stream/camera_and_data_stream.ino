/*** External library header files import ****/
#include "esp_camera.h"
#include <WiFi.h>
#include <WebSocketsServer.h>

/**** Custom setup ******/
#define DEBUG_MODE 1   // to toggle between debug and non-debug modes.
#include "secrets.h"   // load the WiFi credentials and websocket ports
#include "esp32pins.h" // load ESP32-cam pin configurations
#include "common.h"    // load the common global variables to be used

WebSocketsServer camWebSocket = WebSocketsServer(CAM_WEBSOCK_PORT);           // a web socket just to send camera camera feed from ESP32 to System
WebSocketsServer dataTxRxWebSocket = WebSocketsServer(DATA_TxRxWEBSOCK_PORT); // a web socket to send collsion distance from ESP32 -to-> System
                                                                              //    and receive navigation controls from System to ESP32.
WiFiServer server(80);
uint8_t cam_num, data_num;
bool is_connected = false;

// function declartions of the helper files
void setUpPinModes();                                              // of driver.cpp
void configCamera();                                               // of helper.cpp
void streamCamFeed(uint8_t num);                                   // of helper.cpp
void streamCollisionDistFeed(uint8_t num);                         // of helper.cpp
void camWebSocketEvent(uint8_t, WStype_t, uint8_t *, size_t);      // of helper.cpp
void dataTxRxWebSocketEvent(uint8_t, WStype_t, uint8_t *, size_t); // of helper.cpp

/************************ Arduino Functions ************************/
void setup()
{
  Serial.begin(115200);
  setUpPinModes();

  Serial.println("[LOG] Attempting to connect to WiFi with provided credentials..");
  WiFi.begin(SSID, PWD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  String IP = WiFi.localIP().toString();
  Serial.print("[INFO] ESP32's IP address:");
  Serial.println(IP);

  /***************************** Start Web server ************************************/
  Serial.println("[LOG] Attempting to start web server ...");
  server.begin();
  Serial.println("[LOG] Web server started ...");

  /****************** Start Websockets for duplex data transfer *********************/
  Serial.println("[LOG] Attempting to start web server ...");
  camWebSocket.begin();
  camWebSocket.onEvent(camWebSocketEvent);
  dataTxRxWebSocket.begin();
  dataTxRxWebSocket.onEvent(dataTxRxWebSocketEvent);
  Serial.printf("[LOG] Started websockets for camera and data tx+rx at ports %d and %d ports respectively.\n", CAM_WEBSOCK_PORT, DATA_TxRxWEBSOCK_PORT);

  configCamera();
}

void loop()
{
  // stream camera feed from ESP32 to System
  camWebSocket.loop();
  // send and receive data: ESP32 <--> System
  dataTxRxWebSocket.loop();
  if (is_connected == true)
  {
    // stream camera feed..
    streamCamFeed(cam_num);
    // stream ultrasonic collision distance feed..
    streamCollisionDistFeed(data_num);
  }
}

// src: for camera streaming http://www.iotsharing.com/2020/03/demo-48-using-websocket-for-camera-live.html
//      for receiving data from the client: https://forum.arduino.cc/t/websocketserver-parsing-and-using-payload/631151
//            - idea of parsing the received data using JSON- https://techtutorialsx.com/2017/11/05/esp32-arduino-websocket-server-receiving-and-parsing-json-content/
// -- a suggestion: not to use strings. instead use integers.

/**
 * Legend for console(here SerialMonitor) messages
 *  - LOG:  A information to register system events. Later will be useful to debuggin purpose - where error occured.]
 *  - INFO: A information that is to be conveyed to user.
 *
 */