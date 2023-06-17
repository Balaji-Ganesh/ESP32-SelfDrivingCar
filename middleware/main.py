# This file is from the branch `experiments` as `fastapi_as_api_in_class.py`
from fastapi import FastAPI, APIRouter
from communication import ESP32Manager, WebManager, ConnectionManager
import uvicorn

app = FastAPI()
esp32_mngr = ESP32Manager(esp32IP='192.168.182.165')
conn_mngr = ConnectionManager()
web = WebManager()
app.mount('/', web.socket_app) # mounting the socketio app to fastapi

app.include_router(esp32_mngr.router)
app.include_router(web.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.2", port=8500)
