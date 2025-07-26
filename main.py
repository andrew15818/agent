from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(move_router)
