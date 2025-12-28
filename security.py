from typing import Optional, Literal, Union, Annotated, Dict, Any
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()



# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'token')

# class User(BaseModel):
#     username: str
#     email: str
#     full_name: str | None = None
#     disabled: bool | None = None

# async def fake_decode_token(token):
#     return(
#         User(
#             username= token + 'fakedecoded',
#             email= "john@example.com",
#             full_name= 'john Doe'
#     ))   

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user

# @app.get('/user/me/')
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user

#-------------------------------------------------------------------------------------

# async def evaluate_token(token: str = Header(..., alias='X-API-key')):
#     if token != 'SECRET_KEY':
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    

# @app.get('/protected-data/', dependencies=[Depends(evaluate_token)])
# async def protected_data():
#     return{'message': 'accepted'}

# -------------------------------------------------------------------------------



# security = HTTPBasic(scheme_name= "Basic Auth for User") # scheme instance

# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     correct_username = "testuser"
#     correct_password = "testpassword"

# # Check credentials
#     if (credentials.username != correct_username or 
#         credentials.password != correct_password):
        
#         # Raise 401 with appropriate headers for Basic Auth challenge
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Basic"}, # Mandatory for Basic Auth challenge
#         )
#     return credentials.username # Return the authenticated username

# @app.get("/users/me")
# def read_current_user(username: str = Depends(authenticate_user)):
#     return {"username": username, "status": "authenticated"}

# --------------------------------------------------------------------------------------------


# security = HTTPBasic()

# USER_DB = {
#     "admin": {"password": "secretadmin", "role": "admin"},
#     "testuser": {"password": "testpassword", "role": "user"}
# }

# async def authenticate_and_get_role(credentials: HTTPBasicCredentials = Depends(security)):
#     user_info = USER_DB.get(credentials.username)

#     if  user_info['password'] != credentials.password or not user_info:
#         raise HTTPException(
#             status_code=401,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Basic'}
#         ) 
#     return user_info['role']


# async def get_user_role(role: str = Depends(authenticate_and_get_role)):
#     if role != 'admin':
#         raise HTTPException(
#             status_code=403,
#             detail='You do not have administrative privileges'

#         )

# @app.get('/admin_area/', dependencies=[Depends(get_user_role)])
# async def read_admin_area():
#     return{'message': 'welcome to the admin dashboard'}

# ----------------------------------------------------------------------------------
security = HTTPBasic()

USER_DB: Dict[str, Dict[str, Any]] = {
    "101": {"id": 101, "name": "Alice", "credits": 150},
    "102": {"id": 102, "name": "Bob", "credits": 50},
    "103": {"id": 103, "name": "Charlie", "credits": 99}
}


async def get_user_profile(X_user_id: str = Header(..., alias='X-User-ID')):
    user_data = USER_DB.get(X_user_id)
    if not user_data:

        raise HTTPException(
            status_code=404, 
            detail="User ID not found"
        )
    return user_data


@app.get("/user/profile")
def get_profile_status(user: Dict[str, Any] = Depends(get_user_profile)):
    # It's good practice to copy the data before modifying it
    response_data = user.copy() 
    
    # Business Logic based on injected data
    if user["credits"] < 100:
        response_data["alert"] = "Action required: Your credit balance is low."
        
    return response_data
























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