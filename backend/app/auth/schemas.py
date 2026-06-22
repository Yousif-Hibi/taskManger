from pydantic import BaseModel ,Field
from datetime import datetime
import uuid 

class UserCreateModel(BaseModel):
    username:str = Field(max_length = 50)
    first_name : str = Field(max_length = 25)
    last_name : str= Field(max_length = 25)
    email:str = Field(max_length = 50)
    password:str = Field(min_length = 6)

class UserModel(BaseModel):
    uid : uuid.UUID 
    username : str 
    email : str 
    first_name : str
    last_name : str
    is_verified : bool 
    password_hash : str = Field(exclude=True)
    created_at: datetime 
    upgraded_at : datetime 
    
class UserLoginModel(BaseModel):
    email : str = Field(max_lenght=40)
    password : str = Field(min_length=6)