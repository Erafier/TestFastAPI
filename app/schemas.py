from fastapi import Body
from pydantic import BaseModel


class Item(BaseModel):
    cargo_type: str
    rate: float

