from fastapi import FastAPI
from app.routers.move_router import move_router

app = FastAPI()

app.include_router(move_router)
