from typing import Optional, Literal, Union, Annotated
from uuid import uuid4
from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie, Form, File, UploadFile, Depends, Request
from datetime import datetime, timezone
import time
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
@app.middleware('http')
async def log_middleware( request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f'Request: {request.method}{request.url}- Duration:{duration:.4f}secondes')
    return response
    


@app.get('/ping/')
async def ping():
    return {'message': 'pong'}    






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