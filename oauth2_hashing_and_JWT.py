from typing import Optional, Literal, Union, Annotated, Dict, Any
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone, timedelta
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# SECRET_PASSWORD_RAW = "supersecret"
# USER_HASHED_PASSWORD = hash_password(SECRET_PASSWORD_RAW)


# print(f"Original Password: {SECRET_PASSWORD_RAW}")
# print(f"Hashed Password: {USER_HASHED_PASSWORD}")
# print("-" * 20)

# # Test 1: Correct password
# is_verified_correct = verify_password("supersecret", USER_HASHED_PASSWORD)
# print(f"Verification with 'supersecret': {is_verified_correct}") # Expected: True

# # Test 2: Incorrect password
# is_verified_incorrect = verify_password("wrongpassword", USER_HASHED_PASSWORD)
# print(f"Verification with 'wrongpassword': {is_verified_incorrect}") # Expected: False
# ---------------------------------------------------------------------------------------------

JWT_SECRET_KEY = "your-super-secret-key-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: Dict[str, str]) -> str:
    # 1. Get a copy of the payload data
    to_encode = data.copy()
    
    # Set expiration time (iat is "issued at")
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    
    # 2. Encode the token
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, str]:
    try:
        # Decode and validate token (including expiration check)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # If token is invalid (bad signature, expired, etc.)
        return {} # Return an empty dict to signal failure
    
# username_data = {"sub": "testuser"} # 'sub' is standard for subject


# # --- Test Section ---
# # Example data (username)
# token = create_access_token(username_data)
# print(f"Generated JWT: {token}")

# decoded_payload = decode_access_token(token)
# print(f"Decoded Payload: {decoded_payload}")

# ----------------------------------------------------------------------------------------------------

# 1. Simulated DB with HASHED Password (Hash of "testpassword")
TEST_PASSWORD_HASH = pwd_context.hash("testpassword")
DUMMY_USER_DB = {"testuser": TEST_PASSWORD_HASH}


# Pydantic model for the response structure
class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    stored_hash = DUMMY_USER_DB.get(form_data.username)
    plain_password_truncated = form_data.password[:71]
    # 1. Authenticate using Hashed Password Verification
    if stored_hash is None or not verify_password(plain_password_truncated, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username or password"
        )
    
    # 2. Success: Create a new JWT token
    access_token = create_access_token(
        data={"sub": form_data.username} # 'sub' is the authenticated user's name
    )
    
    # 3. Return the standard OAuth2 token response
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # 2. Decode and validate the token
    payload = decode_access_token(token) 
    
    # 3. Check for decoding failure (JWTError, expiration, bad signature)
    if not payload:
        # Also catches cases where payload is empty (JWTError handled by decode_access_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials (Token invalid or expired)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get username from payload (sub is the standard field)
    username: str | None = payload.get("sub")
    
    # Check if 'sub' field exists
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing user identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 4. Return the authenticated username
    return username


@app.get("/jwt-protected")
def read_jwt_protected_data(username: str = Depends(get_current_user)):
    """
    This route is fully protected by JWT validation, expiration, and signature checks.
    """
    return {
        "message": "Access granted via valid JWT", 
        "current_user": username
    }






















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