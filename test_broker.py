from app.models.paper_account import PaperAccount
from app.broker.paper_broker import PaperBroker


account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

broker = PaperBroker()

account = broker.buy(
    account=account,
    symbol="AAPL",
    quantity=1.5,
    price=100
)

print("After buy:")
print(account)

account = broker.sell(
    account=account,
    symbol="AAPL",
    quantity=0.5,
    price=120
)

print("\nAfter sell:")
print(account)