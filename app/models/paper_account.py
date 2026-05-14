from pydantic import BaseModel
from app.models.position import Position
from app.models.trade import Trade


class PaperAccount(BaseModel):
    cash_balance: float
    positions: list[Position]
    trades: list[Trade]