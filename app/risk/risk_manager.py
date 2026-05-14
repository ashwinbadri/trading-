from pydantic import BaseModel
from app.models.paper_account import PaperAccount


class RiskDecision(BaseModel):
    approved: bool
    reason: str


class RiskManager:

    def can_buy(
        self,
        account: PaperAccount,
        symbol: str,
        quantity: float,
        price: float
    ) -> RiskDecision:

        cost = quantity * price

        if account.cash_balance < cost:
            return RiskDecision(
                approved=False,
                reason="Insufficient cash balance"
            )

        existing_position = next(
            (p for p in account.positions if p.symbol == symbol.upper()),
            None
        )

        if existing_position is not None:
            return RiskDecision(
                approved=False,
                reason="Already holding this stock"
            )

        max_position_cost = account.cash_balance * 0.20

        if cost > max_position_cost:
            return RiskDecision(
                approved=False,
                reason="Trade exceeds max 20% cash allocation"
            )

        return RiskDecision(
            approved=True,
            reason="Risk checks passed"
        )