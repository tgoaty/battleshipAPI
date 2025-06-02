from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from database import get_db
app = FastAPI(
    title="battleship API",
    version="1.0.0",
    debug=True
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)