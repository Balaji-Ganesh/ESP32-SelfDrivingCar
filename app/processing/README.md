This folder contains the scripts which
- **Communication**
    - Establishes the communication with ESP32
    - Gets the camera and ultra-sonic feed from ESP32
    - Sends the navigation controls to ESP32
- **Processing**
    - Performs image processing on the camera feed and detects
        - traffic lights and their status
        - lane detection
    - this and along with ultra-sonic feed, makes navigation controls.