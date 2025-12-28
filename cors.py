from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# allowed_origins = [
#     "https://frontend.example.com",
#     "http://localhost:8080",
# ]

# # 1, 2. Add CORSMiddleware and configure for all origins and methods
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_origins, 
#     allow_credentials=True, # Allow cookies/authentication headers (not strictly required for *)
#     allow_methods=["GET", "POST"], # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"], # Allow all headers
# )



# @app.get("/data")
# def read_data():
#     return {"message": "CORS is enabled for all domains."}


# class Item(BaseModel):
#     name: str

# # 3. Test Routes
# @app.get("/items")
# def list_items():
#     return {"items": ["item1", "item2"]}

# @app.post("/create")
# def create_item(item: Item):
#     return {"message": f"Item '{item.name}' created successfully."}

# -------------------------------------------------------------------------------------------------------------

# allowed_origins_single = [
#     "https://internal.app.com",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_origins_single, # Restricted list (mandatory when allow_credentials=True)
#     allow_credentials=True, # Allows sending Authorization header, cookies, etc.
#     allow_methods=["GET", "POST"],
#     # Explicitly allow standard headers and custom headers needed for authentication
#     allow_headers=["Authorization", "Content-Type", "X-Custom-Auth"], 
# )

# # Test Route that requires the custom header (simulating authentication)
# @app.get("/auth-check")
# def auth_check(custom_auth: str = Header(..., alias="X-Custom-Auth")):
#     if custom_auth != "ValidKey":
#         raise HTTPException(status_code=403, detail="Invalid X-Custom-Auth")
#     return {"message": "Access granted with custom header."}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.middleware("http")
async def custom_cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin")
    
    # 1. Proceed with request flow
    response = await call_next(request)
    
    # 2. Check for the Super Secret Origin
    if origin == "https://super-secret-admin.com":
        # Allow Super Secret Origin to access its own content (standard ACAO behavior)
        response.headers["Access-Control-Allow-Origin"] = origin
        
    # 3. Conditional block for all other Origins
    elif origin:
        # For any other origin, redirect them to use a specific public mirror
        # NOTE: This logic is for demo only. Standard CORS requires ACAO to match Origin or be '*'
        response.headers["Access-Control-Allow-Origin"] = "https://public-mirror.com"
        
    # Also add standard CORS response headers for preflight requests if needed (simplified here)
    response.headers["Access-Control-Allow-Methods"] = "GET, POST" 
    
    return response

# Test Route
@app.get("/sensitive-resource")
def sensitive_resource():
    return {"data": "This resource is CORS-controlled by custom logic."}




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