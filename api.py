from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from main import find_buyers


class Inputs(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

s = np.array([[1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0],
              [0, 1, 1, 1, 0],
              [1, 0, 0, 0, 1]])
w = np.array([1, 4, 5, 6, 2]) # quantity
p = np.array([[10, 3, 4, 2, 1],
             [11, 3, 5, 3, 2],
             [9, 3, 3, 7, 3],
             [12, 3, 4, 6, 1]]) # price of 1 item in each shop

distance = np.array([3, 2, 2, 3]) # distance from the shop
pdist_cost = 2 # price of gas


app = FastAPI()

@app.post("/compute_routes/")
async def compute_routes(inputs: Inputs):



    buyers = find_buyers()
    return buyers