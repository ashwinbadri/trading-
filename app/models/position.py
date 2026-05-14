from pydantic import BaseModel


class Position(BaseModel):
    symbol: str
    quantity: float
    average_price: float