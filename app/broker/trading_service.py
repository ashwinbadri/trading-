from app.broker.paper_broker import PaperBroker
from app.memory.trade_repository import TradeRepository
from app.models.paper_account import PaperAccount


class TradingService:

    def __init__(self):
        self.broker = PaperBroker()
        self.trade_repository = TradeRepository()

    def buy(
        self,
        account: PaperAccount,
        symbol: str,
        quantity: float,
        price: float
    ) -> PaperAccount:

        updated_account = self.broker.buy(
            account=account,
            symbol=symbol,
            quantity=quantity,
            price=price
        )

        latest_trade = updated_account.trades[-1]

        self.trade_repository.save_trade(latest_trade)

        return updated_account

    def sell(
        self,
        account: PaperAccount,
        symbol: str,
        quantity: float,
        price: float
    ) -> PaperAccount:

        updated_account = self.broker.sell(
            account=account,
            symbol=symbol,
            quantity=quantity,
            price=price
        )

        latest_trade = updated_account.trades[-1]

        self.trade_repository.save_trade(latest_trade)

        return updated_account