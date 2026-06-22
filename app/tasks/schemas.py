from pydantic import BaseModel
from datetime import datetime ,date
import uuid

class Task(BaseModel) :
    uid : uuid.UUID
    user_id : int
    title : str
    description : str
    status : str
    due_date : date
    created_at: datetime 
    update_at : datetime 

class TaskCreateModel(BaseModel):
    user_id : int
    title : str
    description : str
    status : str
    due_date : str

  
class TaskUpdater(BaseModel) :
    user_id : int
    title : str
    description : str
    status : str
    due_date : date
    
