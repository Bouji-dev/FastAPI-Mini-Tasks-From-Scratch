from typing import Optional, Literal, Union, Annotated, Dict, Any
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

# async def get_token(token: str = Depends(oauth2_scheme)):
#     return token

# @app.get('/docs-test/')
# async def read_token_test(token_string: str = Depends(get_token)):
#     return {"message": "Bearer Token received successfully", "token": token_string[:10] + "..."}

# ------------------------------------------------------------------------------------------------

# VALID_TOKEN ='fake-token'
# USERNAME_MAPPING = {VALID_TOKEN: "token-user"}


# async def authenticate_token(token: str = Depends(oauth2_scheme)):
#     if token != VALID_TOKEN:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return USERNAME_MAPPING[token]

# @app.get("/user/info")
# def get_user_info(username: str = Depends(authenticate_token)):
#     return {"message": f"Authenticated successfully", "username": username}

# --------------------------------------------------------------------------------------

# DUMMY_USER_DB = {"admin": "password"} 
# STATIC_TOKEN = "fake-token"

# @app.post("/token")
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password
    
#     # 2. Authenticate against the dummy DB
#     if DUMMY_USER_DB.get(username) != password:
#         # 4. Return 400 Bad Request on login failure (OAuth2 standard)
#         raise HTTPException(
#             status_code=400, 
#             detail="Incorrect username or password"
#         )
    
#     # 3. Success: Return the token in the standard OAuth2 format
#     token_response: Dict[str, Any] = {
#         "access_token": STATIC_TOKEN,
#         "token_type": "bearer"
#     }
#     return token_response
# --------------------------------------------------------------------------------


DUMMY_USER_DB = {"admin": "password"} 
VALID_TOKEN = "fake-token"
USERNAME_MAPPING = {VALID_TOKEN: "admin"} # Map the token back to the username

# Dependency from Task 2 (for protected routes)
def authenticate_token(token: str = Depends(oauth2_scheme)):
    if token != VALID_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return USERNAME_MAPPING[token]

# Path Operation from Task 3 (Token generation)
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if DUMMY_USER_DB.get(form_data.username) != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": VALID_TOKEN,
        "token_type": "bearer"
    }

# 2, 3, 4. The protected route using the Dependency
@app.get("/protected-resource", status_code=status.HTTP_200_OK)
def read_protected_resource(username: str = Depends(authenticate_token)):
    """
    This route is protected by the Bearer token dependency.
    """
    return {
        "status": "access granted", 
        "data": f"Hello, {username}! This data is highly secured by OAuth2."
    }




















#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
def run() -> None:
    import uvicorn
    from pathlib import Path

    current_module_name = Path(__file__).name[:-3]

    uvicorn.run(
        f"{current_module_name}:app",
        host="0.0.0.0",
        port=11111,
        reload=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    run()