from fastapi import FastAPI, Query, HTTPException, status, Depends, Path
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Address(BaseModel):
    city: set
    zip_code: str


class Customer(BaseModel):
    name: str
    shipping_address: Address


class Tag(BaseModel):
    name:str
    id: int


class ProductDetail(BaseModel):
    product_name: str
    tags: list[Tag]


class CompanySetting(BaseModel):
    billing_address: Optional[Address] = None


class Order(BaseModel):
    customer: Customer


@app.post('/customers/')
async def customer_info(customer: Customer):
    return {'status': 'customer created', 'name': customer.name , 'city': customer.shipping_address.city }    

@app.post('/product-details/')
async def add_product(details: ProductDetail):
    return{'product': details.product_name, 'tag_count': len(details.tags)}

@app.put('/company/{company_id}/setting/')
async def company_setting(address: CompanySetting, company_id: int = Path(..., gt=0) ):
    return{'company id': company_id, 'company billing address':address.billing_address.city}


@app.post('/orders/{order_id}/')
async def orders(order_data:Order, order_id: str, promo_code: Optional[str] = None,  ):
    return { 'order id': order_id, 'promo code': promo_code, 'customer name': order_data.customer.name }