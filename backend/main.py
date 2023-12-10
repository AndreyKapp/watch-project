from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from api import base_router
from app import app_router
from settings import STATIC_ROOT


app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name="static")
app.include_router(base_router)
app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
