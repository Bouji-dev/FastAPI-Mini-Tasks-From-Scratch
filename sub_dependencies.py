from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends
from datetime import datetime, timezone

app = FastAPI()


async def get_user_id(user_id: int):
    return user_id

async def get_user_role(user_id: int = Depends(get_user_id)):
    if user_id % 2 == 0:
        role = 'Admin'
    else:
        role = 'Regular'
    return role    


@app.get('/role/')
async def get_role(
    role: str = Depends(get_user_role)):
    return {'role': role}





async def get_token(x_token: str | None = Header(None)):
    return x_token


async def get_user(token = Depends(get_token)):
    if token == 'abc123':
        return {'id': 1 , 'role': 'admin'}
    if token == 'guest':
        return { 'id': 2, 'role': 'guest'}
    return None

async def get_permissions(user = Depends(get_user)):
    if user is None:
        return 'no_access'
    if user['role'] == 'admin':
        return 'full_access'
    if user['role'] == 'guest':
        return 'read_only'
    
@app.get('/check/')
async def check_permissions(
    permission: str = Depends(get_permissions)
):
    return {'permission': permission}



# class LoginData(BaseModel):
#     username: str
#     password: str

# async def validate_login( data: LoginData):
#     if not data.username:
#         raise HTTPException(status_code=400, detail='username not found')
#     if len(data.password) < 6 :
#         raise HTTPException(status_code= 400 , detail='password must be greater than 6 characters')
#     return data    

# async def get_user_role( valid = Depends(validate_login)):
#     if valid.username == 'admin':
#         role = 'admin'
#     else:
#         role = 'user'

#     return role


# @app.post('/login/')
# async def login(role = Depends(get_user_role)):
#     return {'role': role}




async def get_token2(x_token: str = Header()):
    return x_token

async def get_query2(q: str | None = Query()):
    return q

async def get_user2(token = Depends(get_token2), query = Depends(get_query2)):
    return f'user with token {token} and query {query}'

@app.post('/info/')
async def info(user = Depends(get_user2) ):
    return user



async def get_token():
    return "mytoken"

class TokenService:
    def __init__(self, token:str = Depends(get_token) ):
        self.token = token



class UserService:
    def __init__ (self, token_service: TokenService = Depends()):
        self.token_service = token_service

@app.get('/service-user/')
async def service_user(user_service: UserService = Depends()):
    return {'token': user_service.token_service.token}


















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