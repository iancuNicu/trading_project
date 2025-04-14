from fastapi import FastAPI
from database import create_db_and_tables
from routers.main import api_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("Application startup...")
    await create_db_and_tables()
    print("Finished startup tasks.")

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

app.include_router(api_router)
