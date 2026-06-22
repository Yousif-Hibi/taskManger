from fastapi import FastAPI
from .tasks.routes import task_router
from contextlib import asynccontextmanager
from app.db.task_db import init_db
from app.auth.routes import auth_router 


@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ....")
    await init_db()
    yield 
    print(f"server is stopped")
    

version = "v1"

app = FastAPI(
    title="Task Manager" ,
    description="site to manage tasks made by team",
    version= version,
    lifespan= life_span
)

app.include_router(task_router ,prefix="/api/task",tags=['tasks'])
app.include_router(auth_router ,prefix="/api/auth",tags= ['auth'])
app.include_router(task_router ,prefix="/api/project",tags=['projects'])
