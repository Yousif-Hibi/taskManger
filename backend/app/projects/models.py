from typing import List
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql  as pg
from datetime import datetime ,date
import uuid

class Project(SQLModel , table=True) :
    __tablename__="project"
    
    uid : uuid.UUID = Field(
        sa_column=Column(
           pg.UUID,
           nullable=False,
           primary_key=True,
           default=uuid.uuid4
        )
    )
    project_name : str
    task_ids : List[uuid.UUID] = Field(
        default_factory=list,
        sa_column=Column(pg.ARRAY(pg.UUID(as_uuid=True)))
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    update_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    
    
    
    def __repr__(self):
        return f"<Project {self.project_name}>"
    
    
 