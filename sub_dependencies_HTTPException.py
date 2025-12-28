from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends
from datetime import datetime, timezone

app = FastAPI()



async def verify_token(x_token: str = Header(...)):
    if x_token == 'invalid':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return x_token

@app.get('/check-token/')
async def check_token(token: str = Depends(verify_token)):
    return {'token': token}




async def get_current_user(token: str = Depends(verify_token)):
    return f'user_for_{token}'

@app.get('/user/me/')
async def user_me(user: str = Depends(get_current_user)):
    return user



class UserService:
    def __init__(self, token: str = Depends(verify_token)):
        self.token = token

    def get_user_info(self):
        return f'info_for_user_with_token_{self.token}'
        

@app.get('/user-service/')
async def user_service(user: UserService = Depends()):
    return {'info': user.get_user_info()}



class AuthService:
    def __init__(self, token: str = Depends(verify_token)):
        self.token = token
        

async def get_additional_data():
    return 'extra_data'

@app.get('/full-info/')
async def full_info(Auth: AuthService = Depends(), data: str = Depends(get_additional_data)):
    return {
        'token': Auth.token,
        'extra data': data
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