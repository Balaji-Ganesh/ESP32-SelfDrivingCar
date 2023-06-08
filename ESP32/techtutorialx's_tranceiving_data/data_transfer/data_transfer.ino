#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

WiFiServer server(80);
WebSocketsServer webSocketsServer(82);

const char *ssid = "********";
const char *password = "********";

void handleReceivedMessage(String message)
{

    StaticJsonBuffer<500> JSONBuffer;                     // Memory pool
    JsonObject &parsed = JSONBuffer.parseObject(message); // Parse message

    if (!parsed.success())
    { // Check for errors in parsing

        Serial.println("Parsing failed");
        return;
    }

    const char *sensorType = parsed["sensor"];           // Get sensor type value
    const char *sensorIdentifier = parsed["identifier"]; // Get sensor type value
    const char *timestamp = parsed["timestamp"];         // Get timestamp
    int value = parsed["value"];                         // Get value of sensor measurement

    Serial.println();
    Serial.println("----- NEW DATA FROM CLIENT ----");

    Serial.print("Sensor type: ");
    Serial.println(sensorType);

    Serial.print("Sensor identifier: ");
    Serial.println(sensorIdentifier);

    Serial.print("Timestamp: ");
    Serial.println(timestamp);

    Serial.print("Sensor value: ");
    Serial.println(value);

    Serial.println("------------------------------");
}

void setup()
{

    Serial.begin(115200);

    delay(2000);

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
// Try just sending and parsing a string -- in a formatted manner.