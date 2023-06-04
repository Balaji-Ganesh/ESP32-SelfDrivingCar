### Short Description
- This model uses ESP32 module as an alternative for RPi and Arduino.
- The camera feed is captured by the ESP32 with its OV2640 camera 
- This feed is streamed over websockets to `System` and controls of navigation after processing in `System`.

#### A Note:
- `System` folder scripts are to be run in a machine capable of processing - like RPi, Laptop, Desktop.
- `ESP32` folder sketches are to be uploaded in ESP32 using Arduino IDE.