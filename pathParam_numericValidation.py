from fastapi import FastAPI, Query, HTTPException, status, Path
from pydantic import BaseModel , Field
from typing import Optional

app = FastAPI()

class Transaction(BaseModel):
    amount: float = Field(...,gt=0)


@app.get('/inventory/{product_id}/')
async def get_inventory(product_id: int = Path(..., ge=100)):
    return {'product id': product_id, 'status': 'Inventory details fetched'}

@app.get('/check-score/{score}')
async def check_score(score: float = Path(..., gt=0, lt=1)):
    return{'score': score, 'result': 'score is valid between 0 and 1'}

@app.get('/reports/{report_id}')
async def report(report_id: int = Path(...,ge= 1000, le=9999), priority: int = Query(...,ge=1, le=5)):
    return {'report id': report_id, 'priority': priority, 'message': 'Report details fetched'}

@app.post('/transfer/{sender_id}/{receiver_id}/')
async def transfer(transaction: Transaction, sender_id: int = Path(..., gt=0), receiver_id:int = Path(..., gt=0)):
    return {'sender': sender_id, 'receiver': receiver_id, 'amount': transaction.amount, 'status': 'Transaction initiated'}