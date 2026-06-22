from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional, List
from .schemas import Task, TaskUpdater, TaskCreateModel
from app.db.task_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.tasks.service import TaskService
from .models import Task
from app.auth.dependencies import AccessTokenBearer

task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()


@task_router.get("/", response_model=List[Task])
async def get_all_tasks(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    print(user_details)
    tasks = await task_service.get_all_tasks(session)
    return tasks


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Task)
async def create_task(
    task_data: TaskCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    new_task = await task_service.create_task(task_data, session)
    return new_task


@task_router.get("/{task_uid}", response_model=Task)
async def get_task(
    task_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    task = await task_service.get_task(task_uid, session)
    if task:
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")


@task_router.patch("/{task_uid}", response_model=Task)
async def update_task(
    task_uid: str,
    task_update: TaskUpdater,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    task = await task_service.update_task(task_uid, task_update, session)
    if task:
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")


@task_router.delete("/{task_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    task = await task_service.delete_task(task_uid, session)
    if task:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
