from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional, List
from .schemas import Project, ProjectUpdater, ProjectCreateModel
from app.db.task_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.projects.service import ProjectService
from .models import Project
from app.auth.dependencies import AccessTokenBearer

project_router = APIRouter()
project_service = ProjectService()
access_token_bearer = AccessTokenBearer()


@project_router.get("/", response_model=List[Project])
async def get_all_projects(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    print(user_details)
    projects = await project_service.get_all_projects(session)
    return projects


@project_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Project)
async def create_project(
    project_data: ProjectCreateModel,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    new_project = await project_service.create_project(project_data, session)
    return new_project


@project_router.get("/{project_uid}", response_model=Project)
async def get_project(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    project = await project_service.get_project(project_uid, session)
    if project:
        return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")


@project_router.patch("/{project_uid}", response_model=Project)
async def update_project(
    project_uid: str,
    project_update: ProjectUpdater,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
) -> dict:
    project = await project_service.update_project(project_uid, project_update, session)
    if project:
        return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")


@project_router.delete("/{project_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    project = await project_service.delete_project(project_uid, session)
    if project:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
