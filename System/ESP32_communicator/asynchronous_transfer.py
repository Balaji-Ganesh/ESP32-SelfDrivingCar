import websocket
import json
 
ws = websocket.WebSocket()
ws.connect("ws://172.168.1.132:81")

print("Connected to the server")

myDict = {
  "s": 256,
  "d": "U",
  "i": 40
}
 
ws.send(json.dumps(myDict))
result = ws.recv()
print(result)
 
ws.close()

# This script, for just sending one time -- send and quit.