from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional, List
from .schemas import Task, TaskUpdater, TaskCreateModel
from app.db.task_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.tasks.service import TaskService
from app.db.models import Task
from app.auth.dependencies import AccessTokenBearer , RoleChecker
from app.errors import TaskNotFound



task_router = APIRouter()
task_service = TaskService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends( RoleChecker(['admin',"user"]))


@task_router.get("/", response_model=List[Task], dependencies=[role_checker])
async def get_all_tasks(
    session: AsyncSession = Depends(get_session),
    token_details: dict =Depends(access_token_bearer),
) -> dict:
    
    tasks = await task_service.get_all_tasks(session)
    return tasks 


@task_router.get("/user/{user_uid}", response_model=List[Task], dependencies=[role_checker])
async def get_user_all_tasks(
    user_uid:str ,
    session: AsyncSession = Depends(get_session),
    token_details: dict =Depends(access_token_bearer),
    
) -> dict:
    
    tasks = await task_service.get_user_tasks(user_uid,session)
    return tasks 


@task_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Task, dependencies=[role_checker])
async def create_task(
    task_data: TaskCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    user_id = token_details.get('user')['user_uid']
    new_task = await task_service.create_task(task_data,user_id,session)
    return new_task


@task_router.get("/{task_uid}", response_model=Task, dependencies=[role_checker])
async def get_task(
    task_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    task = await task_service.get_task(task_uid, session)
    if task:
        return task
    raise TaskNotFound()


@task_router.patch("/{task_uid}", response_model=Task, dependencies=[role_checker])
async def update_task(
    task_uid: str,
    task_update: TaskUpdater,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    task = await task_service.update_task(task_uid, task_update, session)
    if task:
        return task
    raise TaskNotFound()


@task_router.delete("/{task_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_task(
    task_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    task = await task_service.delete_task(task_uid, session)
    if task:
        return
    raise TaskNotFound()
