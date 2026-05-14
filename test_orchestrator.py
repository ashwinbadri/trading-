from app.models.paper_account import PaperAccount
from app.orchestrator.trading_orchestrator import TradingOrchestrator


account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

orchestrator = TradingOrchestrator()

watchlist = ["AAPL", "TSLA", "NVDA"]

for symbol in watchlist:
    account = orchestrator.process_symbol(
        account=account,
        symbol=symbol
    )

print("\nFinal Portfolio")
print(account)