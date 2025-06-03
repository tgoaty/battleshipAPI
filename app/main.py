from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from .init_db import init_db

app = FastAPI(
    title="battleship API",
    version="1.0.0",
    debug=True
)



@asynccontextmanager
async def startup():
    await init_db()
    yield


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
