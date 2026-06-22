from typing import Optional
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql  as pg
from datetime import datetime ,date
import uuid

class Task(SQLModel , table=True) :
    __tablename__="task"
    
    uid : uuid.UUID = Field(
        sa_column=Column(
           pg.UUID,
           nullable=False,
           primary_key=True,
           default=uuid.uuid4
        )
    )
    assigned_to: int | None = Field(default=None)
    title : str
    description : str
    status : str
    due_date : date
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    update_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    parent_task_id : Optional[uuid.UUID] = Field(default=None, foreign_key="task.uid")
    
    
    
    def __repr__(self):
        return f"<Task {self.title}>"
    
    
 