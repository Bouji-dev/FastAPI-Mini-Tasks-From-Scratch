from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form
from datetime import datetime, timezone

app = FastAPI()

@app.post('/login-form/')
async def login_form(username: str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': password}


@app.post('/feedback/')
async def feedback(message: str = Form(...), category: str = Form('general')):
    return {'message': message, 'category': category}

@app.post('/submit/')
async def submit(title: str = Form(...), content: str = Form(...), published: bool = False):
    return {
        "title": title,
        "content": content,
        "published": published
    }

class PostData(BaseModel):
    title: str
    body: str
    tags: list[str]


@app.post('/create-post/')
async def create_post(title: str = Form(...), body: str = Form(...), tags: list[str]= []):
    return PostData(title=title, body=body, tags=tags)    



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