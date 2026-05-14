from sqlalchemy import select

from app.memory.database import SessionLocal
from app.memory.db_models import PaperAccountEntity, PositionEntity, TradeEntity
from app.models.paper_account import PaperAccount
from app.models.position import Position
from app.models.trade import Trade, TradeAction


DEFAULT_ACCOUNT_ID = "default"
DEFAULT_STARTING_CASH = 10_000.0


class AccountRepository:

    def get_account(self) -> PaperAccount:
        db = SessionLocal()

        try:
            account_entity = db.get(PaperAccountEntity, DEFAULT_ACCOUNT_ID)

            if account_entity is None:
                account_entity = PaperAccountEntity(
                    id=DEFAULT_ACCOUNT_ID,
                    cash_balance=DEFAULT_STARTING_CASH
                )
                db.add(account_entity)
                db.commit()

            positions = [
                Position(
                    symbol=entity.symbol,
                    quantity=entity.quantity,
                    average_price=entity.average_price
                )
                for entity in db.scalars(select(PositionEntity)).all()
            ]

            trade_entities = db.scalars(
                select(TradeEntity).order_by(TradeEntity.timestamp)
            ).all()

            trades = [
                Trade(
                    symbol=entity.symbol,
                    action=TradeAction(entity.action),
                    quantity=entity.quantity,
                    price=entity.price,
                    timestamp=entity.timestamp
                )
                for entity in trade_entities
            ]

            return PaperAccount(
                cash_balance=account_entity.cash_balance,
                positions=positions,
                trades=trades
            )

        finally:
            db.close()

    def save_account(self, account: PaperAccount):
        db = SessionLocal()

        try:
            account_entity = db.get(PaperAccountEntity, DEFAULT_ACCOUNT_ID)

            if account_entity is None:
                account_entity = PaperAccountEntity(id=DEFAULT_ACCOUNT_ID)
                db.add(account_entity)

            account_entity.cash_balance = account.cash_balance

            db.query(PositionEntity).delete()

            for position in account.positions:
                db.add(
                    PositionEntity(
                        symbol=position.symbol,
                        quantity=position.quantity,
                        average_price=position.average_price
                    )
                )

            db.commit()

        finally:
            db.close()
