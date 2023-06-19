/*** External library header files import ****/
#include "esp_camera.h"
#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

/**** Custom setup ******/
#define DEBUG_MODE 1 // to toggle between debug and non-debug modes.
#define CAM_WEBSOCK_PORT 81
#define DATA_TxRxWEBSOCK_PORT 82
#include "secrets.h" // load the WiFi credentials

/*** Configuring Pins of ESP32 cam for camera support *****/
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27

#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

WebSocketsServer camWebSocket = WebSocketsServer(CAM_WEBSOCK_PORT);           // a web socket just to send camera camera feed from ESP32 to System
WebSocketsServer dataTxRxWebSocket = WebSocketsServer(DATA_TxRxWEBSOCK_PORT); // a web socket to send collsion distance from ESP32 -to-> System
                                                                              //    and receive navigation controls from System to ESP32.
WiFiServer server(80);
uint8_t cam_num, data_num;
bool is_connected = false;

/******************************************** Helpers **********************************************/
/////// WebSocket Events...
void camWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length)
{
  switch (type)
  {
  case WStype_DISCONNECTED:
    Serial.printf("[INFO] Camera client - [%u]: Disconnected!\n", num);
    is_connected = false;
    break;
  case WStype_CONNECTED:
    cam_num = num;
    is_connected = true;
    Serial.printf("[INFO] Camera client - [%u]: Connected!\n", num);
    break;

  case WStype_TEXT:
  case WStype_BIN:
  case WStype_ERROR:
  case WStype_FRAGMENT_TEXT_START:
  case WStype_FRAGMENT_BIN_START:
  case WStype_FRAGMENT:
  case WStype_FRAGMENT_FIN:
    break;
  }
}

void dataTxRxWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length)
{
  // local function declaration
  void parseNavigationControls(char *json);

  switch (type)
  {
  case WStype_DISCONNECTED:
    Serial.printf("[INFO] dataTxRx client - [%u]: Disconnected!\n", num);
    break;
  case WStype_CONNECTED:
    data_num = num;
    is_connected = true;
    Serial.printf("[INFO] dataTxRx client - [%u]: Connected!\n", num);
    break;
  // get the message and echo back
  case WStype_TEXT:
#ifdef DEBUG_MODE
    Serial.printf("[%u] Received data: %s\nParsed data:", num, payload);
#endif
    parseNavigationControls((char *)payload);
    break;
  case WStype_BIN:
  case WStype_ERROR:
  case WStype_FRAGMENT_TEXT_START:
  case WStype_FRAGMENT_BIN_START:
  case WStype_FRAGMENT:
  case WStype_FRAGMENT_FIN:
    break;
  }
}

// Other helpers
void configCamera()
{
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 9;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK)
  {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
}

void streamCamFeed(uint8_t num)
{
  // capture a frame
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb)
  {
    Serial.println("Frame buffer could not be acquired");
    return;
  }
  // replace this with your own function
  camWebSocket.sendBIN(num, fb->buf, fb->len);

  // return the frame buffer back to be reused
  esp_camera_fb_return(fb);
}

void parseNavigationControls(char *json)
{
  StaticJsonDocument<96> doc;                              // Memory pool. Size is based on estimation by https://arduinojson.org/v6/assistant/#/step1 for data
  DeserializationError error = deserializeJson(doc, json); // deserialization

  if (error)
  {
    Serial.print(F("deserializeJson() failed with code "));
    Serial.println(error.c_str());
    return;
  }

  // Get value of sensor measurement
  long speed = doc["s"];
  String direction = doc["d"]; // 0: UP, 1: Down, 2:LEFT, 3: Right
  long interval = doc["i"];

  Serial.println();
  Serial.println("----- NEW DATA FROM CLIENT ----");

  Serial.print("Speed: ");
  Serial.println(speed);

  Serial.print("Direction: ");
  Serial.println(direction);

  Serial.print("Interval: ");
  Serial.println(interval);

  Serial.println("------------------------------");
}

void streamCollisionDistFeed(uint8_t num)
{
  // setup of ultra-sonic..
  // for now sending some dummy data.
  // unsigned int collisionDistance = 85;
  // uint8_t *payload = &collisionDistance; // ultra-sonic distance
  String payload = "85";
  dataTxRxWebSocket.sendTXT(num, payload);

  // in actual version..
  //    handle the collision here itself. Just for the information purpose, send it to the system.
}

/************************ Arduino Functions ************************/
void setup()
{
  Serial.begin(115200);

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