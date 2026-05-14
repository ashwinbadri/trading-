from datetime import datetime
from app.models.paper_account import PaperAccount
from app.models.position import Position
from app.models.trade import Trade, TradeAction


class PaperBroker:

    def buy(
        self,
        account: PaperAccount,
        symbol: str,
        quantity: float,
        price: float
    ) -> PaperAccount:
        cost = quantity * price

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if price <= 0:
            raise ValueError("Price must be greater than 0")

        if account.cash_balance < cost:
            raise ValueError("Insufficient cash balance")

        updated_positions = self._add_to_position(
            account.positions,
            symbol,
            quantity,
            price
        )

        trade = Trade(
            symbol=symbol.upper(),
            action=TradeAction.BUY,
            quantity=quantity,
            price=price,
            timestamp=datetime.now()
        )

        return PaperAccount(
            cash_balance=account.cash_balance - cost,
            positions=updated_positions,
            trades=account.trades + [trade]
        )

    def sell(
        self,
        account: PaperAccount,
        symbol: str,
        quantity: float,
        price: float
    ) -> PaperAccount:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if price <= 0:
            raise ValueError("Price must be greater than 0")

        updated_positions = self._remove_from_position(
            account.positions,
            symbol,
            quantity
        )

        trade = Trade(
            symbol=symbol.upper(),
            action=TradeAction.SELL,
            quantity=quantity,
            price=price,
            timestamp=datetime.now()
        )

        return PaperAccount(
            cash_balance=account.cash_balance + quantity * price,
            positions=updated_positions,
            trades=account.trades + [trade]
        )

    def _add_to_position(
        self,
        positions: list[Position],
        symbol: str,
        quantity: float,
        price: float
    ) -> list[Position]:
        symbol = symbol.upper()
        updated = []

        found = False

        for position in positions:
            if position.symbol == symbol:
                total_quantity = position.quantity + quantity
                total_cost = (
                    position.quantity * position.average_price
                    + quantity * price
                )
                new_average_price = total_cost / total_quantity

                updated.append(
                    Position(
                        symbol=symbol,
                        quantity=total_quantity,
                        average_price=new_average_price
                    )
                )
                found = True
            else:
                updated.append(position)

        if not found:
            updated.append(
                Position(
                    symbol=symbol,
                    quantity=quantity,
                    average_price=price
                )
            )

        return updated

    def _remove_from_position(
        self,
        positions: list[Position],
        symbol: str,
        quantity: float
    ) -> list[Position]:
        symbol = symbol.upper()
        updated = []
        found = False

        for position in positions:
            if position.symbol == symbol:
                found = True

                if position.quantity < quantity:
                    raise ValueError("Cannot sell more shares than currently held")

                remaining_quantity = position.quantity - quantity

                if remaining_quantity > 0:
                    updated.append(
                        Position(
                            symbol=symbol,
                            quantity=remaining_quantity,
                            average_price=position.average_price
                        )
                    )
            else:
                updated.append(position)

        if not found:
            raise ValueError("No position found for symbol")

        return updated