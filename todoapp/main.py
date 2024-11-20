from fastapi import FastAPI  # type: ignore
from .model import *  # Change to relative import
from .database import *  # Change to relative import
from .routers import auth, todos  # Change to relative import

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)