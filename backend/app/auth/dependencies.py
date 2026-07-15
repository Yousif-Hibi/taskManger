from fastapi.security import HTTPBearer
from fastapi import Request ,status ,Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from app.errors import InvalidToken
from .utils import decode_token
from fastapi.exceptions import HTTPException
from app.db.redis import token_in_blocklist
from app.db.task_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List
from app.db.models import User
from app.errors import(
    InvalidToken , 
    RefreshTokenRequierd,
    AccessTokenRequierd, 
    InsufficientPermission
)

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self , auto_error = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None :        
        
        creds = await super().__call__(request)
        if not creds:
            return None
        token = creds.credentials 
        token_data = decode_token(token)
        
        if not self.token_vaild(token):
            raise InvalidToken()
        
        if await token_in_blocklist(token_data['jti']):
            raise InvalidToken() 
 
        self.verify_token_data(token_data)


        return token_data
    
    def token_vaild(self,token : str)->bool :
        
        token_data = decode_token(token)
        return token_data is not None 
    
    def verify_token_data(self,token_data):
        
        raise NotImplementedError("Override in child classes")
    
    
    
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict)-> None:
        if token_data and token_data['refresh'] : 
            raise AccessTokenRequierd()

class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self,token_data:dict)-> None:
        if token_data and not token_data['refresh'] : 
            raise RefreshTokenRequierd()

async def get_currect_user(token_detaols:dict = Depends(AccessTokenBearer()),
session : AsyncSession = Depends(get_session)
):
    user_email = token_detaols['user']['email']
    user = await user_service.get_user_by_email(user_email,session)
    
    return user


class RoleChecker:
    def __init__(self,allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles
    

    def __call__(self, current_user:User= Depends(get_currect_user)) :
        if current_user.role in self.allowed_roles :
            return True
        raise InsufficientPermission()
        