from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str 
    price: float 


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class Order(BaseModel):
    item_id: int
    quantity: int = 1


class Inventory(BaseModel):
    item_name: str
    stock: int

@app.post('/items')
async def read_items(item: Item):
    return{'message': 'Item created successfully', 'item': item}

@app.put('/products/{product_id}/')
async def get_product(product_id: int, product: ProductUpdate):
    return{'message': f'Product {product_id} created successfully', 'product':product}

@app.post('/orders/')
async def get_order(order: Order):
    return {'status': 'order placed', 'order details': order}

@app.post('/inventory/{warehouse_id}/')
async def add_inventory(warehouse_id: str, inventory: Inventory, force: bool = False):
    return{'status': f'Inventory with warehouse id:{warehouse_id} created','force update': force , 'details': inventory.model_dump()}