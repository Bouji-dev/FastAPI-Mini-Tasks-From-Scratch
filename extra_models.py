from typing import Optional, Literal, Union
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie
from datetime import datetime, timezone

app = FastAPI()

class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    name: str
    age: int
    address: Address

@app.post('/user-info/')
async def user_info(user: User):
    return user    

class Person (BaseModel):
    name: str
    email: str


class Employee(Person):
    salary: float

@app.post('/employee/')
async def create_employee(emp: Employee):
    return emp


class Order(BaseModel):
    id: str = Field(default_factory= lambda:uuid4().hex)
    items: list[str]
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

@app.post('/order/')
async def create_order(order: Order):
    return order

class Car(BaseModel):
    type: Literal['car']
    brand: str
    model: str 

class Bike(BaseModel):
    type: Literal['bike']
    brand: str
    is_electric: bool

@app.post('/vehicle/', response_model= Car | Bike)
async def create_vehicle(data: Car | Bike):
    return data    











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