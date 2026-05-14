from pydantic import BaseModel

from app.market.market_data_provider import (
    MarketDataProvider,
    StockData
)


class TradeSignal(BaseModel):
    symbol: str
    action: str
    confidence: float
    reason: str


class MomentumTradingSkill:

    def __init__(self):
        self.market_data_provider = MarketDataProvider()

    def analyze(self, symbol: str) -> TradeSignal:

        stock_data: StockData = (
            self.market_data_provider.get_stock_data(symbol)
        )

        if stock_data.day_change_percent <= -3:

            return TradeSignal(
                symbol=symbol,
                action="BUY",
                confidence=0.75,
                reason=(
                    "Stock dropped significantly today "
                    "which may indicate a momentum dip opportunity."
                )
            )

        return TradeSignal(
            symbol=symbol,
            action="HOLD",
            confidence=0.60,
            reason="No strong momentum signal detected."
        )