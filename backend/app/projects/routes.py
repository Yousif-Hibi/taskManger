from fastapi import FastAPI, APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import Optional, List
from .schemas import Project, ProjectUpdater, ProjectCreateModel
from app.db.task_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.projects.service import ProjectService
from app.db.models import Project
from app.auth.dependencies import AccessTokenBearer , RoleChecker
from app.errors import ProjectNotFound

project_router = APIRouter()
project_service = ProjectService()
access_token_bearer = AccessTokenBearer()
role_checker =Depends( RoleChecker(['admin',"user"]))

@project_router.get("/", response_model=List[Project] , dependencies=[role_checker])
async def get_all_projects(
    session: AsyncSession = Depends(get_session),
   token_details: dict =Depends(access_token_bearer),
) :
    
    projects = await project_service.get_all_Projects(session)
    return projects


@project_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Project, dependencies=[role_checker])
async def create_project(
    project_data: ProjectCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) :
    user_id = token_details.get('user')['user_uid']
    new_project = await project_service.create_Project(project_data,user_id,session)
    return new_project


@project_router.get("/{project_uid}", response_model=Project, dependencies=[role_checker])
async def get_project(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    project = await project_service.get_Project(project_uid, session)
    if project:
        return project
    raise ProjectNotFound()


@project_router.patch("/{project_uid}", response_model=Project, dependencies=[role_checker])
async def update_project(
    project_uid: str,
    project_update: ProjectUpdater,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
) -> dict:
    project = await project_service.update_Project(project_uid, project_update, session)
    if project:
        return project
    raise ProjectNotFound()


@project_router.delete("/{project_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_project(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    project = await project_service.delete_Project(project_uid, session)
    if project:
        return
    raise ProjectNotFound()
