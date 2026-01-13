from fastapi import FastAPI
import socketio

from app.core.ws.ws_manager import sio
from app.controllers.orders_controller import router as orders_router

import app.handlers.orders_handler

fastapi_app = FastAPI(title="Multi-Layered Server")

fastapi_app.include_router(orders_router)


@fastapi_app.get("/")
async def root():
    return {"message": "Multi-Layered Server is running"}


app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path='/ws')
