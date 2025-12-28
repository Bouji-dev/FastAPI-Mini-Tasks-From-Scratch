from fastapi import FastAPI, status, HTTPException

#from pydantic import EmailStr
app = FastAPI()

def validate_username(username):
    valid = True
    errors = []
    if len(username) < 8:
        valid = False
        errors.append('username length must be greater than 8 characters')
    return valid , errors

def validate_password(password):
    valid = True
    errors = []
    if len(password) < 8 or len(password) > 15:
        valid = False
        errors.append('password length must be between 8-15 characters')

    if (password.upper() == password or password.lower() == password ):
        valid = False
        errors.append('password must contain both upper and lower letters')
    
    return valid , errors

def validate_email(email):
    valid = True
    errors = []
    return valid, errors
    
def validate_data(username, password, email):
    valid = True
    errors = []

    user_is_valid , user_errors= validate_username(username)
    password_is_valid, password_errors = validate_password(password)
    emial_is_valid, email_errors = validate_email(email)
    
    valid = (user_is_valid and password_is_valid and emial_is_valid)
    errors = password_errors + user_errors + email_errors

    return valid, errors

@app.post('/signup/')
async def signup_user(username:str, password:str, email:str):
    is_valid, errors = validate_data(username, password, email)

    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,  detail=errors)
       
    
    return {'status': status.HTTP_201_CREATED , 'message': 'user created'}