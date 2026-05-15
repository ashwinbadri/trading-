import os

import httpx
from pydantic import BaseModel


class StockData(BaseModel):
    symbol: str
    current_price: float
    day_change_percent: float
    volume: int


class MarketDataProvider:
    DATA_BASE_URL = "https://data.alpaca.markets/v2"
    DEFAULT_TIMEOUT_SECONDS = 10.0

    def __init__(self):
        self.api_key = os.getenv("APCA_API_KEY_ID")
        self.secret_key = os.getenv("APCA_API_SECRET_KEY")

    def _get_headers(self) -> dict[str, str]:
        if not self.api_key or not self.secret_key:
            raise RuntimeError(
                "Alpaca credentials are missing. Set APCA_API_KEY_ID "
                "and APCA_API_SECRET_KEY."
            )

        return {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }

    def _get_latest_bar(self, symbol: str) -> dict:
        response = httpx.get(
            f"{self.DATA_BASE_URL}/stocks/bars/latest",
            params={"symbols": symbol.upper(), "feed": "iex"},
            headers=self._get_headers(),
            timeout=self.DEFAULT_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        bars = response.json().get("bars", {})
        latest_bar = bars.get(symbol.upper())

        if latest_bar is None:
            raise ValueError(f"No latest bar returned for symbol {symbol.upper()}")

        return latest_bar

    def _get_recent_bars(self, symbol: str, limit: int = 2) -> list[dict]:
        response = httpx.get(
            f"{self.DATA_BASE_URL}/stocks/{symbol.upper()}/bars",
            params={
                "timeframe": "1Day",
                "limit": limit,
                "feed": "iex"
            },
            headers=self._get_headers(),
            timeout=self.DEFAULT_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        bars = response.json().get("bars", [])

        if not bars:
            raise ValueError(f"No recent bars returned for symbol {symbol.upper()}")

        return bars

    def _calculate_day_change_percent(
        self,
        latest_close: float,
        previous_close: float
    ) -> float:
        if previous_close == 0:
            return 0.0

        return ((latest_close - previous_close) / previous_close) * 100

    def get_stock_data(self, symbol: str) -> StockData:
        latest_bar = self._get_latest_bar(symbol)
        recent_bars = self._get_recent_bars(symbol)

        if len(recent_bars) >= 2:
            previous_close = recent_bars[-2]["c"]
        else:
            previous_close = latest_bar["o"]

        current_price = latest_bar["c"]
        day_change_percent = self._calculate_day_change_percent(
            latest_close=current_price,
            previous_close=previous_close
        )

        return StockData(
            symbol=symbol.upper(),
            current_price=current_price,
            day_change_percent=day_change_percent,
            volume=latest_bar["v"]
        )
