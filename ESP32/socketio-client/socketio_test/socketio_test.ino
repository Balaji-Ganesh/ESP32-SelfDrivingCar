// adopted from: https://github.com/Valgueiro/esp32_SocketIO/blob/master/socketIO.ino
#include <Arduino.h>

#include <WiFi.h>
#include <WiFiMulti.h>

#include <SocketIoClient.h>

#define USE_SERIAL Serial

WiFiMulti WiFiMulti;
SocketIoClient webSocket;

// CONST VARIABLES
const char *ssid = "SSID";
const char *pass = "PASSWORD";
const char *HOST = "HOST_IP";
// In this experiment, when python-socketion is ran on 127.0.0.2:8500 it is not connected.
// but later when changed the host of python-socket to 0.0.0.0, then got some messages exchange, but with a lot of errors.
const int PORT = 8500;

void event(const char *payload, size_t length){
    USE_SERIAL.printf("got message: %s\n", payload);
}

void setup(){
    USE_SERIAL.begin(9600);

    USE_SERIAL.setDebugOutput(true);

    USE_SERIAL.println();
    USE_SERIAL.println();
    USE_SERIAL.println();

    for (uint8_t t = 4; t > 0; t--){
        USE_SERIAL.printf("[SETUP] BOOT WAIT %d...\n", t);
        USE_SERIAL.flush();
        delay(1000);
    }   


    // Connect to WIFI
    WiFiMulti.addAP(ssid, pass);

    while (WiFiMulti.run() != WL_CONNECTED){
        delay(100);
    }

    // Receive events from server
    webSocket.on("event", event);

    webSocket.begin(HOST, 8500, "/bar/foo");
}

int count = 0;

void loop(){
    webSocket.loop();
    count++;
    if (count == 18000){
        count = 0;

        // Send data to Server
        webSocket.emit("status", "Hello from esp32!");
    }
}