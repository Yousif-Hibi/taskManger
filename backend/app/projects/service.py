from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ProjectCreateModel ,ProjectUpdater
from sqlmodel import select ,desc
from .models import Project
from datetime import datetime

class ProjectService:
    async def get_all_Projects(self, session:AsyncSession):
        statement = select(Project).order_by(desc(Project.created_at))
        result = await session.exec(statement)
        return result.all()
    
    
    async def get_Project(self,Project_uid:str, session:AsyncSession):
        statement = select(Project).where(Project.uid == Project_uid)
        result = await session.exec(statement)
        Project = result.first()
        return Project if not None else None
    
    
    async def create_Project(self,Project_data:ProjectCreateModel,session:AsyncSession):
        Project_data_dict = Project_data.model_dump()
        new_Project =Project(
            **Project_data_dict
        )
        session.add(new_Project)
        await session.commit()
        return new_Project
    
    async def update_Project(self,Project_uid:str,update_Project:ProjectUpdater, session:AsyncSession):
        Project_to_update = await self.get_Project(Project_uid,session)
        if Project_to_update is not None:
            update_data_dict = update_Project.model_dump()
            for k,v in update_data_dict.items():
                setattr(Project_to_update,k,v)
            await session.commit()
            return Project_to_update
        else :
            return None
            
    
    async def delete_Project(self,Project_uid:str, session:AsyncSession):
        Project_to_delete = await self.get_Project(Project_uid,session)
        if Project_to_delete is not None:
            await session.delete(Project_to_delete)
            await session.commit()
        else:
            return