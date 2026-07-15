from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from .tasks.routes import task_router
from .projects.routes import project_router
from contextlib import asynccontextmanager
from app.db.task_db import init_db
from app.auth.routes import auth_router 
from .errors import (
    RevokedToken,
    TasksException,
    create_exption_handler,
    InvaildCredentials,
    TaskNotFound,
    ProjectNotFound,
    UserAlreadyExists,UserNotFound,
    AccessTokenRequierd ,RefreshTokenRequierd,InsufficientPermission,InvalidToken
    
)

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ....")
    await init_db()
    yield 
    print(f"server is stopped")
    

version = "v1"

app = FastAPI(
    title="Task Manager" ,
    description="site to manage tasks made by team",
    version= version,
    
)
app.add_exception_handler(
    InvaildCredentials,
    create_exption_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Invalid email or password",
            "error_code": "invalid_credentials"
        }
    )
)

app.add_exception_handler(
    InvalidToken,
    create_exption_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Token is invalid or expired",
            "error_code": "invalid_token"
        }
    )
)

app.add_exception_handler(
    RevokedToken,
    create_exption_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "This token has been revoked",
            "error_code": "token_revoked"
        }
    )
)

app.add_exception_handler(
    AccessTokenRequierd,
    create_exption_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Please provide a valid access token",
            "error_code": "access_token_required"
        }
    )
)

app.add_exception_handler(
    RefreshTokenRequierd,
    create_exption_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        initial_detail={
            "message": "Please provide a valid refresh token",
            "error_code": "refresh_token_required"
        }
    )
)

# ---------------------------------------------------------
# Authorization Errors
# ---------------------------------------------------------
app.add_exception_handler(
    InsufficientPermission,
    create_exption_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "You do not have permission to perform this action",
            "error_code": "insufficient_permissions"
        }
    )
)

# ---------------------------------------------------------
# Resource Conflict / Identity Errors
# ---------------------------------------------------------
app.add_exception_handler(
    UserAlreadyExists,
    create_exption_handler(
        status_code=status.HTTP_409_CONFLICT,  # Changed to 409 Conflict as it fits resource duplication better than 403
        initial_detail={
            "message": "A user with this email already exists",
            "error_code": "user_already_exists"
        }
    )
)

# ---------------------------------------------------------
# Not Found Errors
# ---------------------------------------------------------
app.add_exception_handler(
    UserNotFound,
    create_exption_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Requested user could not be found",
            "error_code": "user_not_found"
        }
    )
)

app.add_exception_handler(
    ProjectNotFound,
    create_exption_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Requested project could not be found",
            "error_code": "project_not_found"
        }
    )
)

app.add_exception_handler(
    TaskNotFound,
    create_exption_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message": "Requested task could not be found",
            "error_code": "task_not_found"
        }
    )
)

# ---------------------------------------------------------
# Global/Fallback Base Exception
# ---------------------------------------------------------
app.add_exception_handler(
    TasksException,
    create_exption_handler(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        initial_detail={
            "message": "An unexpected error occurred within the tasks system",
            "error_code": "internal_server_error"
        }
    )
)
@app.exception_handler(500)
async def internal_server_error(reqest,exc):
    return JSONResponse(
        content={ 
            "message": "An unexpected error occurred within the tasks system",
            "error_code": "internal_server_error"
        }
    )

app.include_router(task_router ,prefix="/api/task",tags=['tasks'])
app.include_router(auth_router ,prefix="/api/auth",tags= ['auth'])
app.include_router(project_router ,prefix="/api/project",tags=['projects'])
