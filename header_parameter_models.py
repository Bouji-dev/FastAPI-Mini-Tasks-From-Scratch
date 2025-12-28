from typing import Optional, Literal

from pydantic import BaseModel , Field
from fastapi import FastAPI, Query, HTTPException, status, Path, Header, Cookie


app = FastAPI()

class ClientInfo(BaseModel):
    agent:str
    version: str


@app.get('/client-info/')
async def client_info(
    agent: str = Header(..., alias='User-Agent'),
    version: str = Header(..., alias='X-App-Version')
):
    return ClientInfo(agent=agent, version=version)


class ApiHeaders(BaseModel):
    api_key: str = Field(min_length=10)
    platform: Literal['web', 'android', 'ios']

@app.get('/check-api/')
async def check_api(
    api_key: str = Header(..., alias='X-Api-key'),
    platform: str = Header(..., alias='X-paltform')
):
    return ApiHeaders(api_key=api_key, platform=platform)


class DeviceInfo(BaseModel):
    model: str
    os_version: str


class RequestHeaders(BaseModel):
    device: DeviceInfo
    request_id: str

@app.get('/request-details/')
async def request_detikes(
    model: str = Header(..., alias='X-Device-Model'),
    os_version: str = Header(..., alias='X-Device-Os'),
    request_id: str = Header(..., alias='X-Request-ID')
):
    return RequestHeaders(
        device = DeviceInfo(model= model, os_version= os_version), request_id= request_id      
    )


class SessionContext(BaseModel):
    session_id: str
    user_id: str
    agent: str
    app_version: str

@app.get('/session-context/')
async def session_context(
    session_id: str = Cookie(...),
    user_id: str = Cookie(...),
    agent: str = Header(..., alias='User-Agent'),
    app_version: str = Header(..., alias='X-App-Version')
):
    return SessionContext(
        session_id=session_id,
        user_id=user_id,
        agent=agent,
        app_version=app_version

    )




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