from fastapi import FastAPI
from .database import init_db
from .routers import router

app = FastAPI(title="Task-Management-API",)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()


