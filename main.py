import os
from fastapi import FastAPI
from google import genai
from contextlib import asynccontextmanager
from app.routers.move_router import move_router
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize permanent or shared resources
    load_dotenv()

    app.state.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
    app.state.system_prompt = os.getenv("SYSTEM_PROMPT")
    print(f"System prompt: {app.state.system_prompt}")
    yield
    # Close permanent or shared resources


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(move_router)
