from fastapi import FastAPI, Response,Query, HTTPException, status, Depends, Path, Cookie, Header
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()


class UserCookies(BaseModel):
    session_id: str | None = None
    theme: str | None = None


class AuthCookie(BaseModel):
    session_id: str = Field(..., min_length=10)
    user_level:  Literal["admin", "basic"]


class Preferencese(BaseModel):
    theme: str 
    lang: str 


class UserCookieBundle(BaseModel):
    prefs: Preferencese
    token: str


class SessionInfo(BaseModel):
    session_id: str
    user_id: str
    agent: str



# @app.get("/set-cookies/")
# async def set_cookies(response: Response):
#     # تنظیم کوکی‌های مورد نیاز برای مسیر /nested-cookies/
#     response.set_cookie(key="theme", value="dark", httponly=False) # کوکی theme
#     response.set_cookie(key="lang", value="fa", httponly=False)   # کوکی lang
#     response.set_cookie(key="token", value="my_secure_jwt_token_123", httponly=True) # کوکی token (معمولاً توکن‌ها httponly هستند)
    
#     # پیام موفقیت آمیز
#     return {"message": "Cookies have been set. Now visit /nested-cookies/ to test."}


@app.get('/cookie-model/')
async def cookie_model(session_id: str | None = Cookie(default=None), theme: str | None = Cookie(default=None)):
    
    return UserCookies(session_id = session_id, theme= theme)

@app.get('/auth-cookie/')
async def auth_cookie(
    session_id: str  = Cookie(...),
    user_level: str  = Cookie(...)
):
    return AuthCookie(session_id= session_id, user_level=user_level)
    
@app.get('/nested-cookies/')
async def nested_cookies(
        theme: str = Cookie(...),
        lang: str = Cookie(...),
        token: str = Cookie(...)
):
    return UserCookieBundle(prefs=Preferencese(theme=theme, lang=lang), token=token)


@app.get('/session-details/')
async def session_details(
     session_id: str = Cookie(...),
     user_id:str = Cookie(...),
     agent: str = Header(...)   
):
    return SessionInfo( 
        session_id= session_id,
        user_id=user_id,
        agent=agent
    )