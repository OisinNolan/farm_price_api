from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Inputs(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.post("/compute_routes/")
async def compute_routes(inputs: Inputs):
    return item