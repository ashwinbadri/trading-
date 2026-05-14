from app.skills.momentum_trading_skill import (
    MomentumTradingSkill
)

from app.models.paper_account import PaperAccount

from app.broker.trading_service import (
    TradingService
)

from app.risk.risk_manager import (
    RiskManager
)


account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

skill = MomentumTradingSkill()
service = TradingService()
risk_manager = RiskManager()

watchlist = [
    "AAPL",
    "TSLA",
    "NVDA"
]

for symbol in watchlist:

    signal = skill.analyze(symbol)

    print(f"\nSignal for {symbol}")
    print(signal)

    if signal.action == "BUY":

        risk_decision = risk_manager.can_buy(
            account=account,
            symbol=symbol,
            quantity=1,
            price=100
        )

        print("Risk Decision:")
        print(risk_decision)

        if risk_decision.approved:

            print(f"Executing BUY for {symbol}")

            account = service.buy(
                account=account,
                symbol=symbol,
                quantity=1,
                price=100
            )

        else:

            print(
                f"Trade rejected: "
                f"{risk_decision.reason}"
            )

print("\nFinal Portfolio")
print(account)