from typing import Optional, Literal, Union
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie
from datetime import datetime, timezone

app = FastAPI()

@app.post('/create-item/', status_code=201 )
async def create_item():
    return {'message': 'item created'}

@app.delete('/itmes/{item_id}/', status_code=204)
async def items(item_id: int):
    return

class Task(BaseModel):
    id: int
    title: str
    done: bool = False


@app.get('/tasks/{task_id}/', response_model= Task)
async def get_tasks(task_id: int):
    if task_id % 2 == 0:
        return {'id': task_id, 'title': 'sample Task', 'status': 200}
        
    raise HTTPException(status_code=404, detail='The Task is odd')

class Login(BaseModel):
    username: str
    password: str


@app.post('/login/')
async def login(data: Login):
    
    if data.username != 'admin':
        raise HTTPException(status_code=404, detail= 'User Not found')
    
    if data.password != '123':
        raise HTTPException(status_code=401, detail= 'Invalid password')    
    return {'message': 'Login ok'}
        



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