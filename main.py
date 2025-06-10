import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers.move_router import move_router
from app.services.move_service import LLMManager, BoardManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize permanent or shared resources
    load_dotenv()

    app.state.llm_manager = LLMManager()
    app.state.board_manager = BoardManager()
    yield
    # Close permanent or shared resources


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(move_router)
