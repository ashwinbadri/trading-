from app.market.market_data_provider import (
    MarketDataProvider
)

from app.broker.trading_service import (
    TradingService
)

from app.memory.trade_repository import (
    TradeRepository
)


market_data_provider = MarketDataProvider()
trading_service = TradingService()
trade_repository = TradeRepository()


tool_registry = {

    "get_stock_data": {
        "description":
            "Get current market data for a stock symbol.",

        "function":
            market_data_provider.get_stock_data
    },

    "get_trades": {
        "description":
            "Get all previous paper trading transactions.",

        "function":
            trade_repository.get_all_trades
    },

    "buy_stock": {
        "description":
            "Execute a paper stock purchase.",

        "function":
            trading_service.buy
    }
}