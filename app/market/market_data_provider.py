from pydantic import BaseModel


class StockData(BaseModel):
    symbol: str
    current_price: float
    day_change_percent: float
    volume: int


class MarketDataProvider:

    def get_stock_data(self, symbol: str) -> StockData:

        mock_data = {
            "AAPL": StockData(
                symbol="AAPL",
                current_price=185,
                day_change_percent=-4.2,
                volume=90_000_000
            ),

            "TSLA": StockData(
                symbol="TSLA",
                current_price=172,
                day_change_percent=2.5,
                volume=120_000_000
            ),

            "NVDA": StockData(
                symbol="NVDA",
                current_price=910,
                day_change_percent=-1.1,
                volume=50_000_000
            )
        }

        return mock_data[symbol.upper()]