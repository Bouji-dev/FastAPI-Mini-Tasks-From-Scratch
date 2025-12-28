from fastapi import FastAPI, Query, HTTPException, status, Depends, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Product(BaseModel):
    name: str = Field(..., description= ' name must be unique ')
    price: float = Field(gt=0)


class UserInfo(BaseModel):
    email: str
    age: int = Field(ge=18, le=65)


class FormData(BaseModel):
    token: str = Field(..., min_length=10, max_length=20)


class AppConfig(BaseModel):
    version: str = 'v1.0.0'
    timeout: int = Field(ge=10, le= 300)


@app.post('/product/')
async def create_product(product: Product):
    return {'status': 'product created', 'data': product.model_dump()}    

@app.put('/users/profile/')
async def user_profile(user: UserInfo):
    return {'status': 'Profile updated', 'user email': user.email}


@app.post('/submit/{form_id}/')
async def submition(form_id: int, data: FormData ):
    return{'form_id': form_id, 'token length': len( data.token)}

@app.put('/config/set/')
async def configuration(config: AppConfig, force: bool = False):
    return {'config_applied': config.model_dump(), 'force_update': force}