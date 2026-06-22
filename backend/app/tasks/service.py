from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TaskCreateModel ,TaskUpdater
from sqlmodel import select ,desc
from .models import Task
from datetime import datetime

class TaskService:
    async def get_all_tasks(self, session:AsyncSession):
        statement = select(Task).order_by(desc(Task.created_at))
        result = await session.exec(statement)
        return result.all()
    
    
    async def get_task(self,task_uid:str, session:AsyncSession):
        statement = select(Task).where(Task.uid == task_uid)
        result = await session.exec(statement)
        task = result.first()
        return task if not None else None
    
    
    async def create_task(self,task_data:TaskCreateModel,session:AsyncSession):
        task_data_dict = task_data.model_dump()
        new_task =Task(
            **task_data_dict
        )
        new_task.due_date = datetime.strptime(task_data_dict['due_date'],"%Y-%m-%d").date()
        session.add(new_task)
        await session.commit()
        return new_task
    
    async def update_task(self,task_uid:str,update_task:TaskUpdater, session:AsyncSession):
        task_to_update = await self.get_task(task_uid,session)
        if task_to_update is not None:
            update_data_dict = update_task.model_dump()
            for k,v in update_data_dict.items():
                setattr(task_to_update,k,v)
            await session.commit()
            return task_to_update
        else :
            return None
            
    
    async def delete_task(self,task_uid:str, session:AsyncSession):
        task_to_delete = await self.get_task(task_uid,session)
        if task_to_delete is not None:
            await session.delete(task_to_delete)
            await session.commit()
        else:
            return