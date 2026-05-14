from app.models.paper_account import PaperAccount
from app.broker.trading_service import TradingService


account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

service = TradingService()

account = service.buy(
    account=account,
    symbol="AAPL",
    quantity=1.25,
    price=100
)

print("Updated account:")
print(account)

print("\nTrade saved to database.")