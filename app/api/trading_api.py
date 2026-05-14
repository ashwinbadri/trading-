from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.models.paper_account import PaperAccount
from app.broker.trading_service import TradingService
from app.memory.trade_repository import TradeRepository


router = APIRouter()

account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

service = TradingService()
trade_repo = TradeRepository()


class TradeRequest(BaseModel):
    symbol: str
    quantity: float
    price: float


@router.post("/buy")
def buy(request: TradeRequest):
    global account

    try:
        account = service.buy(
            account=account,
            symbol=request.symbol,
            quantity=request.quantity,
            price=request.price
        )

        return account

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell")
def sell(request: TradeRequest):
    global account

    try:
        account = service.sell(
            account=account,
            symbol=request.symbol,
            quantity=request.quantity,
            price=request.price
        )

        return account

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolio")
def get_portfolio():
    return account


@router.get("/trades")
def get_trades():
    return trade_repo.get_all_trades()
