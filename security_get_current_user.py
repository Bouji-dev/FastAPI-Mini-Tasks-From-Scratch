from typing import Optional, Literal, Union, Annotated, Dict, Any
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

basic_auth_scheme = HTTPBasic()

# async def get_current_credentials(credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)):
#     return credentials

# @app.get('/whoami/')
# async def who_am_i(creds: HTTPBasicCredentials = Depends(get_current_credentials)):
#     return{'credentioals': {'username': creds.username, 'auth_scheme': creds.model_json_schema}}

# ----------------------------------------------------------------------------

# basic_auth_scheme = HTTPBasic()

# USERS = {
#     "jdoe": "securepass",
#     "test": "12345"
# }

# async def get_validated_username(credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)):
#     if credentials.username in USERS and USERS[ credentials.username ] ==  credentials.password :
#         return credentials.username
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail='Invalid credentials.',
#         headers={'WWW-Authenticate': 'Basic'}
#     )


# @app.get('/welcome/')
# async def welcome(creds: HTTPBasicCredentials = Depends(get_validated_username)):
#     return{ 'message': f'Welcome back, {creds}!, Your access is confirmed' }

# -----------------------------------------------------------------------------------
# USERS_FULL_DB: Dict[str, Dict[str, Any]] = {
#     "alice": {"password": "pwd1", "full_name": "Alice Smith"},
#     "bob": {"password": "pwd2", "full_name": "Bob Johnson"},
#     }


# class User(BaseModel):
#     username: str
#     full_name: str

# async def get_current_user(credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)):
#     user_info = USERS_FULL_DB.get(credentials.username)

#     if not user_info or user_info['password']  != credentials.password:
#         raise HTTPException(
#             status_code=401,
#             detail='Invalid credentials',
#             headers={'WWW-Authenticate': 'Basic'}
#         )  

#     return User(username= credentials.username, full_name=user_info['full_name'])

# @app.get('/my-details')
# async def read_user_details(user: User = Depends(get_current_user)):
#     return {"message": "User details successfully retrieved", 'profile': user}

# -----------------------------------------------------------------------------------------------
USERS_FULL_DB: Dict[str, Dict[str, Any]] = {
    "alice": {"password": "pwd1", "full_name": "Alice Smith", "user_id": 1},
    "bob": {"password": "pwd2", "full_name": "Bob Johnson", "user_id": 2},
}
ITEMS_DB: Dict[int, Dict[str, Any]] = {
    101: {"name": "Alice's Project", "owner_id": 1},
    102: {"name": "Bob's Report", "owner_id": 2},
    103: {"name": "Shared Document", "owner_id": 1},
}

class User(BaseModel):
    username: str
    full_name: str
    user_id: str

async def get_current_user(credentials: HTTPBasicCredentials = Depends(basic_auth_scheme)):
    user_info = USERS_FULL_DB.get(credentials.username)

    if not user_info or user_info['password']  != credentials.password:
        raise HTTPException(
            status_code=401,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Basic'}
        )  

    return User(user_id= user_info['user_id'], username= credentials.username, full_name=user_info['full_name'])


async def verify_item_owner(user: User = Depends(get_current_user), item_id: int = Path(...)):
    item = ITEMS_DB.get(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item['owner_id'] != user.user_id:
        raise HTTPException(
            status_code=403, 
            detail="Not authorized to access this item. You are not the owner."
        )
    return item

@app.get('/items/{item_id}/')
async def read_items(item: Dict[str, Any] = Depends(verify_item_owner)):

    return {"message": "Access granted", "item_details": item}














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