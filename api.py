from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Inputs(BaseModel):
    shop_buys: List[int]
    food_weights: List[int]
    food_prices: List[int]
    shop_distances: List[int]
    gas_price: int

class Visit(BaseModel):
    shop: int
    crops: List[int]

class Output(BaseModel):
    routes: List[List[Visit]]

app = FastAPI()

@app.post("/compute_routes/")
async def compute_routes(inputs: Inputs):
    item: Output = f(...) # David's function goes here
    return item