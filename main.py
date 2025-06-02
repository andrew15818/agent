import os
from fastapi import FastAPI
from google import genai
from contextlib import asynccontextmanager
from app.routers.move_router import move_router
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize permanent or shared resources
    load_dotenv()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    app.state.client = client
    yield

    # Close permanent or shared resources


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(move_router)
