/*
This file acts as a helper to .ino file in handling websocket events.
Few code snippets are adopted from: https://github.com/un0038998/CameraCarWithPanTiltControl/blob/main/Camera_Car_with_PanTilt_Control/Camera_Car_with_PanTilt_Control.ino
*/

#include <WebSocketsServer.h>
#include <sstream>
#include "esp_camera.h"
#include "esp32pins.h" // load ESP32-cam pin configurations
#include "config.h"    // load the configurations for motor controls..
#include "common.h"    // load the common global variables to be used

// ultra sonic setup
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

// Helper function declarations..
void moveCar(int);
/******************************************** Helpers **********************************************/

void parseCameraControls(uint8_t *payload, size_t len)
{
  std::string data = "";
  data.assign((char *)payload, len);
  std::istringstream ss(data);
  std::string key, value;
  std::getline(ss, key, ',');
  std::getline(ss, value, ',');
  Serial.printf("[Camera] Key [%s] Value[%s]\n", key.c_str(), value.c_str());
  int valueInt = atoi(value.c_str());
  // control the stream..
  // if (key == "stream"){
  //   if (value == "begin")
  //     stream_camera = true;
  //   else if(value == "end")
  //     stream_camera = false;
  // }
  // else
  // will be working in next iteration...
  // Idea: The Python server should able to inform ESP32 to begin the stream not.
  //          To avoid unnecessary full of queue.
  // - use global variables for those. In the loop() based on these values, performing streaming.
  if (key == "light")
  {
    ledcWrite(PWMLightChannel, valueInt);
  }
}

void parseNavigationControls(uint8_t *payload, size_t len)
{
  std::string data = "";
  data.assign((char *)payload, len);
  std::istringstream ss(data);
  std::string key, value;
  std::getline(ss, key, ',');
  std::getline(ss, value, ',');
  Serial.printf("[DataTxRx] Key [%s] Value[%s]\n", key.c_str(), value.c_str());
  int valueInt = atoi(value.c_str());
  if (key == "direction") // FIXME: Later shorten to single letter. To reduce payload size.
  {
    moveCar(valueInt);
  }
  else if (key == "speed") // FIXME: Later shorten to single letter. To reduce payload size.
  {
    ledcWrite(PWMSpeedChannel, valueInt);
  }
  // else if (key == "collision"){
  //   if (value == "begin")
  //     stream_collision_feed = true;
  //   else if (value == "end")
  //     stream_collision_feed = false;
  // }
  // Feature for next iteration
  // Idea: The Python server should able to inform ESP32 to begin the stream not.
  //          To avoid unnecessary full of queue.
  else if (key == "interval")
  {
    // theme: for a given direction - till how much time unit, should follow that.
    //   should also allow overriding functionality tooo
    // Currently this functionality in pause.
    //
  }
}

/////// WebSocket Events...
void camWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t len)
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
    parseCameraControls(payload, len);
  case WStype_BIN:
  case WStype_ERROR:
  case WStype_FRAGMENT_TEXT_START:
  case WStype_FRAGMENT_BIN_START:
  case WStype_FRAGMENT:
  case WStype_FRAGMENT_FIN:
    break;
  }
}

void dataTxRxWebSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t len)
{
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
    parseNavigationControls(payload, len);
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

// helper for camera configuration
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

// helpers for streaming..
void streamCollisionDistFeed(uint8_t num)
{
  // setup of ultra-sonic..
  // for now sending some dummy data.
  // unsigned int collisionDistance = 85;
  // uint8_t *payload = &collisionDistance; // ultra-sonic distance
  delay(50);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
  Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
  String payload = "85";
  dataTxRxWebSocket.sendTXT(num, payload);

  // in actual version..
  //    handle the collision here itself. Just for the information purpose, send it to the system.
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
