from typing import Optional, Literal, Union

from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie


app = FastAPI()

class UserOut(BaseModel):
    id: int
    username: str


@app.get('/user/{user_id}', response_model=UserOut)
async def get_user(user_id: int):
    return {'id': user_id, 'username': 'user-test', 'password': '12345'}    


class UserDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str


class UserPublic(BaseModel):
    id: int
    username: str

@app.get('/public-user/{id}', response_model=UserPublic)
async def public_user(id: int):
    return UserDB(
        id=id,
        username='ehsan',
        email='Ehsan@example.com',
        hashed_password='UserDB.hashed_password'
    )

class Product(BaseModel):
    id: int
    title: str

@app.get('/products/', response_model=list[Product])
async def get_products():
    return [
        {'id': 1, 'title': 'Phone', 'price': 300},
        {'id': 2, 'title': 'Tablet', 'price': 600},
        
    ]    

class SuccessResponse(BaseModel):
    status: str = 'ok'
    data: dict

class ErrorResponse(BaseModel):
    status: str = 'error'
    message: str

@app.get('/calc/{num}', response_model= SuccessResponse | ErrorResponse)    
async def calc( num: int):
    if num % 2 == 0:
        return {'status': 'ok', 'data': {'result': num * 2}}
    return {'status': 'error', 'message': 'odd number received'}
    







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