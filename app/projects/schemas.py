from pydantic import BaseModel
from datetime import datetime ,date
import uuid
from typing import List
from sqlmodel import  Field

class Project(BaseModel) :
    uid : uuid.UUID
    project_name : str
    task_ids: List[uuid.UUID] = Field(default_factory=list)
    created_at: datetime 
    update_at : datetime 

class ProjectCreateModel(BaseModel):
    project_name : str
    task_ids: List[uuid.UUID] = Field(default_factory=list)

  
class ProjectUpdater(BaseModel) :
    project_name : str
    task_ids: List[uuid.UUID] = Field(default_factory=list)
    
