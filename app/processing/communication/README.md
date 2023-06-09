### In brief
- These files establishes Websocket duplex communication between ESP32 and system.
- Websocket will be opened on two ports - {81, 82} (in ESP32).
- Multiprocessing is enabled with two processes (on System) on two ports -- so, that communication can take place parallely and have minimum negligible latency.
- Established two websocket are exposed out for other files -- to get and send data through it, as and when needed.

*NOTE*: These scripts is taken from the `experiments` branch of this repository, which are tested individually earlier.
        - to be even more specific - its from `System/ESP32_communicator/`

**External References**
- [Understand the notion of different programming techniques: Threading, Synchronous and Asynchronous ways](https://medium.com/velotio-perspectives/an-introduction-to-asynchronous-programming-in-python-af0189a88bbb)