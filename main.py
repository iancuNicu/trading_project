from fastapi import FastAPI
from database import create_db_and_tables
from routers.main import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

app.include_router(api_router)
