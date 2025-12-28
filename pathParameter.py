from fastapi import FastAPI

app = FastAPI()

@app.get('/items/{item_id}/')
async def read_item(item_id: int):
    return {'item_id': item_id, 'description': 'A valuable item'}

@app.get('/users/{user_name}/')
async def read_user(user_name: str):
    if user_name == 'admin':
        return {'message': 'welcome Administrator'}
    return {'message': f'welcome, {user_name}'}

@app.get('/products/{product_id}/details/{detail_type}/')
async def get_product_id(product_id: int , detail_type: str):
    return {'product id': product_id, 'detail type': detail_type}

@app.get('/files/{file_path:path}/')
async def read_file(file_path:str):
    return {'file_path': file_path}