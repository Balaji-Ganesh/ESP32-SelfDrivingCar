#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

WiFiServer server(80);
WebSocketsServer webSocketsServer(82);

const char *ssid = "KMIT-Colleage";
const char *password = "A1B2C3D4E5";

void handleReceivedMessage(String json)
{
    StaticJsonDocument doc(96);                              // Memory pool
    DeserializationError error = deserializeJson(doc, json); // deserialization

    if (error)
    {
        Serial.print(F("deserializeJson() failed with code "));
        Serial.println(error.c_str());
        return;
    }

    // Get value of sensor measurement
    const char *speed = doc['s'];
    const char *direction = doc['d'];
    int interval = doc['i'];

    Serial.println();
    Serial.println("----- NEW DATA FROM CLIENT ----");

    Serial.print("Speed");
    Serial.println(speed);

    Serial.print("Direction ");
    Serial.println(direction);

    Serial.print("Interval");
    Serial.println(interval);

    Serial.println("------------------------------");
}

void setup()
{
    Serial.begin(115200);
    delay(2000);

    // Setup WiFi connection
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi..");
    }

    Serial.println("Connected to the WiFi network");
    Serial.println(WiFi.localIP());

    server.begin();
    delay(100);
}

void loop()
{

    WiFiClient client = server.available();
    if (client.connected() && webSocketsServer.handshake(client))
    {
        String data;
        while (client.connected())
        {
            data = webSocketsServer.getData();
            if (data.length() > 0)
            {
                handleReceivedMessage(data);
                webSocketsServer.sendData(data);
            }
            delay(10); // Delay needed for receiving the data correctly
        }
        Serial.println("The client disconnected");
        delay(100);
    }
    delay(100);
}

// src: https://techtutorialsx.com/2017/11/05/esp32-arduino-websocket-server-receiving-and-parsing-json-content/
//   NOTE: some upgrades need to be done to the code. Refer: https://arduinojson.org/v6/doc/upgrade/
// Try just sending and parsing a string -- in a formatted manner.