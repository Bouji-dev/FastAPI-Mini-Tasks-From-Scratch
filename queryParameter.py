from fastapi import FastAPI
from typing import Optional, List

app = FastAPI()

@app.get('/search/')
async def search(q: str | None = None):
    if q:
        return {'q': q}
    return{'query': 'No query provided'}

@app.get('/products/')
async def get_products(skip: int = 0,  limit: int = 10 ):
    return {'skip': skip, 'limit': limit}
    
@app.get('/mixed/{item_id}')
async def get_mixed_data(item_id: int, short: bool = False):
    if short:
        return {'message': f'The {item_id} is ok'}
    return{'item_id': item_id, 'description': 'full discription', 'short': short}

@app.post('/multi-query/')
async def multi_query(tags: Optional[List[str]] = None):
    if tags:
        return{'tags': tags, 'counts': len(tags)}
    return {'tags': [], 'count': len(tags), 'message': "No tags provided"}