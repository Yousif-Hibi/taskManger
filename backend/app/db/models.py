from typing import Optional ,List
from sqlmodel import SQLModel, Field, Column ,Relationship
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
    assigned_to: Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")
    title : str
    description : str
    status : str
    due_date : date
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    update_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    parent_task_id : Optional[uuid.UUID] = Field(default=None, foreign_key="task.uid")
    user_uid : Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid",sa_type=pg.UUID)
    user: Optional["models.User"] = Relationship(
        back_populates="created_tasks",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Task.user_uid]"
        }
    )
    assignee: Optional["models.User"] = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Task.assigned_to]" # Tells SQLAlchemy explicitly which key to use
        }
    ) 
    def __repr__(self):
        return f"<Task {self.title}>"
    
    


class User(SQLModel,table=True):
    __tablename__="users"
    
    uid : uuid.UUID = Field(
        sa_column=Column(
           pg.UUID,
           nullable=False,
           primary_key=True,
           default=uuid.uuid4
        )
    )
    username : str 
    email : str 
    first_name : str
    last_name : str
    role : str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False  , server_default="user"
    ))
    is_verified : bool = Field(default= False)
    password_hash : str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    upgraded_at : datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
   
    assigned_tasks: List["models.Task"] = Relationship(
        back_populates="assignee",
        sa_relationship_kwargs={
            "lazy": "selectin",                   # Added lazy loading here
            "foreign_keys": "[Task.assigned_to]"   # Keeps it unambiguous
        }
    )

    created_tasks: List["models.Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[Task.user_uid]"      # Resolves the other foreign key
        }
    )
    def __repr__(self):
        return f"<User {self.username}>"




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
    user_uid : Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")
    
     
    
    def __repr__(self):
        return f"<Project {self.project_name}>"
    
    
 