from fastapi import FastAPI, Request
from .database import engine
from .models import Base
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/health/')
def health():
    return {'status': 'healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
