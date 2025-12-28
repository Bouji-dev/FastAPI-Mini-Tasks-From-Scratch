from fastapi import FastAPI, Query, HTTPException, status, Depends, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Pagination(BaseModel):
    skip:int = 0
    limit: int = 10


class SearchOptions(BaseModel):
    query: Optional[str] = None
    sort_by: str = Field('date', min_length=4)


class InputData(BaseModel):
    data: str


class ProcessingOption(BaseModel):
    async_mode: bool = False


@app.get('/posts/')
async def get_post(params:Pagination = Depends()):
    return{'skip': params.skip, 'limit': params.limit, 'message': 'Fetched posts range'}    

@app.get('/data/advanced/')
async def advanced_search(options: SearchOptions = Depends()):
    return { 'options': options, 'applied': True}

@app.get('/users/{user_id}/orders/')
async def user_order(page: Pagination = Depends(), user_id: int = Path(...,gt=0) ):
    return{ 'user id': user_id, 'page': page , 'message': 'user orders page'}

@app.post('/process-request/')
async def process_request(data: InputData , options: ProcessingOption):
    return {'input': data.model_dump(), 'options': options.model_dump(), 'status': 'Processing complete' }





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