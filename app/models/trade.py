from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class TradeAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Trade(BaseModel):
    symbol: str
    action: TradeAction
    quantity: float
    price: float
    timestamp: datetime