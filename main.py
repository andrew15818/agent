import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from app.routers.move_router import move_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize permanent or shared resources
    load_dotenv()

    # TODO: Make the actual invocation
    app.state.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
    app.state.system_prompt = os.getenv("SYSTEM_PROMPT")
    app.state.move_history = []
    app.state.prompt_template = ChatPromptTemplate(
        [("system", app.state.system_prompt)]
    )
    print(type(app.state.llm))
    print(f"System prompt: {app.state.system_prompt}")
    yield
    # Close permanent or shared resources


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(move_router)
