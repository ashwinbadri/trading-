import json
from typing import Literal

from pydantic import BaseModel, ValidationError

from app.market.market_data_provider import MarketDataProvider
from app.ai.llm_client import LLMClient


class AiTradeSignal(BaseModel):
    symbol: str
    action: Literal["BUY", "HOLD", "SELL"]
    confidence: float
    reason: str


class AiStockAnalysisSkill:

    def __init__(self):
        self.market_data_provider = MarketDataProvider()
        self.llm_client = LLMClient()

    def analyze(self, symbol: str) -> AiTradeSignal:
        stock_data = self.market_data_provider.get_stock_data(symbol)

        raw_response = self.llm_client.analyze_stock(
            symbol=stock_data.symbol,
            current_price=stock_data.current_price,
            day_change_percent=stock_data.day_change_percent,
            volume=stock_data.volume
        )

        try:
            data = json.loads(raw_response)

            return AiTradeSignal(
                symbol=symbol.upper(),
                action=data["action"],
                confidence=data["confidence"],
                reason=data["reason"]
            )

        except (json.JSONDecodeError, KeyError, ValidationError) as e:
            print("Invalid LLM response:")
            print(raw_response)

            return AiTradeSignal(
                symbol=symbol.upper(),
                action="HOLD",
                confidence=0.0,
                reason=f"AI response was invalid, so defaulted to HOLD. Error: {e}"
            )
