from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()





@app.get('/items/search')
async def item_search(keyword: str = Query(min_length=3, max_length=15) ):
    return {"search_term": keyword,"\nmessage": "Search executed successfully"}


@app.get('/filter/')
async def filter_query(prefix: Optional[str] = Query(regex="^[a-z]*$")):
    return{'filter prefix': prefix}

@app.get('/users/status/{user_id}/')
async def user_status(user_id:int,  token:str = Query(min_length=8, max_length=8)):
    return{"user id":user_id,'token': token }

valid_categories= ['A', 'B', 'C']
@app.post('/multi-query/')
async def get_multi_tags(tags: Optional[list[str]] = Query(None, min_length=2), category:str = Query(...)):
    if category not in valid_categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'category must be one of {valid_categories}')
    return {'tags': tags, 'category': category, 'valid tags': tags is not None and all(len(t)>= 2 for t in tags)}


