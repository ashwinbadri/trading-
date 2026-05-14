from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.broker.trading_service import TradingService
from app.memory.account_repository import AccountRepository
from app.memory.trade_repository import TradeRepository


router = APIRouter()

service = TradingService()
trade_repo = TradeRepository()
account_repository = AccountRepository()


class TradeRequest(BaseModel):
    symbol: str
    quantity: float
    price: float


@router.post("/buy")
def buy(request: TradeRequest):
    try:
        account = account_repository.get_account()

        updated_account = service.buy(
            account=account,
            symbol=request.symbol,
            quantity=request.quantity,
            price=request.price
        )

        account_repository.save_account(updated_account)

        return updated_account

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell")
def sell(request: TradeRequest):
    try:
        account = account_repository.get_account()

        updated_account = service.sell(
            account=account,
            symbol=request.symbol,
            quantity=request.quantity,
            price=request.price
        )

        account_repository.save_account(updated_account)

        return updated_account

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portfolio")
def get_portfolio():
    return account_repository.get_account()


@router.get("/trades")
def get_trades():
    return trade_repo.get_all_trades()
