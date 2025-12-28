from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile
from datetime import datetime, timezone

app = FastAPI()


class LoginData(BaseModel):
    username: str
    password: str


@app.post('/login-model')
async def login_model(
    username: str = Form(...),
    password: str = Form(...)

):
    
    return LoginData(username=username, password=password)

class ProfileUpdate(BaseModel):
    bio: str | None = None
    location: str | None = None


@app.post('/update-profile/')    
async def update_profile(
    bio: str | None = Form(None),
    location: str | None = Form(None)
):
    return ProfileUpdate(bio=bio, location=location)


class ArticleData(BaseModel):
    title: str
    content: str


@app.post('/article/')
async def create_article(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(...)
):
    return { 'data': ArticleData(title=title, content=content),
            'filename': image.filename
    }


class Author(BaseModel):
    name: str
    email: str


class BlogPost(BaseModel):
    title: str
    body: str
    author: Author

@app.post('/create-blog/')    
async def create_blog(
    title: str = Form(...),
    body: str = Form(...),
    author_name: str = Form(...),
    author_email: str = Form(...)
):
    author = Author(name=author_name, email=author_email)
    return BlogPost(title=title, body=body, author=author)










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