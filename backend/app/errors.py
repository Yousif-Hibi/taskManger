
from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse



class TasksException(Exception):
    pass

class InvalidToken(TasksException):
    pass

class RevokedToken(TasksException):
    pass

class AccessTokenRequierd(TasksException):
    pass

class RefreshTokenRequierd(TasksException):
    pass

class UserAlreadyExists(TasksException):
    pass

class InsufficientPermission(TasksException):
    pass 

class ProjectNotFound(TasksException):
    pass

class TaskNotFound(TasksException):
    pass

class InvaildCredentials(TasksException):
    pass

class UserNotFound(TasksException):
    pass

def create_exption_handler(status_code:int, initial_detail:Any) -> Callable[[Request, Exception], JSONResponse]:
    
    async def expction_handler(reqest: Request,exc: TasksException): 
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return expction_handler