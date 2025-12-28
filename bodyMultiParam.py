from fastapi import FastAPI, Query, HTTPException, status, Depends, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str]= None


class User(BaseModel):
    username: str = Field(..., min_length= 5)
    password: str


class UpdateData(BaseModel):
     data: dict


class Setting(BaseModel):
    active: bool
    environment: str = 'prod'

@app.post('/items/{item_id}/')
async def get_item_multi( item_id: int , item: Item = Item(name='', description='')  , priority: int = 1 ):
    return {'item id': item_id, 'priority': priority, 'item': item.model_dump(), 'message': 'Item created'}

@app.post('/login/')
async def login(client_id: int , user: User):
    return{'client id': client_id, 'user': user, 'message': f'user{user.username}logged in '}

@app.put('/resource/{resource_id}/{version}/')
async def resource(data: UpdateData, resource_id: int = Path(..., gt=0), version: int = Path(..., gt=0), ):
    return{'id': resource_id, 'version': version, 'update_data': data.data}

@app.post('/config/')
async def config(setting: Setting, user_token:str = Query(...,description="Authentication token")):
    return {'setting': setting , 'token_used': user_token}