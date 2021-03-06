from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from main import find_buyers as find_buyers_
from mock_input import inputs_

class Inputs(BaseModel):
    shop_buys: List[List[int]]
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

@app.post("/find_buyers/")
async def find_buyers(inputs: Inputs):
    i = inputs_
    ordered_buyer_list: Output = find_buyers_(
        i.shop_buys,
        i.food_weights,
        i.food_prices,
        i.shop_distances,
        i.gas_price
    )
    return ordered_buyer_list