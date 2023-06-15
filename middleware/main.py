# This file is from the branch `experiments` as `fastapi_as_api_in_class.py`
from fastapi import FastAPI, APIRouter
from communication import ESP32Manager, WebManager
import uvicorn
app = FastAPI()
esp32 = ESP32Manager(esp32IP='192.168.134.165')
web = WebManager()

app.include_router(esp32.router)
app.include_router(web.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.2", port=8500)
