import uuid

from app.memory.database import SessionLocal
from app.memory.db_models import TradeEntity
from app.models.trade import Trade


class TradeRepository:

    def save_trade(self, trade: Trade):
        db = SessionLocal()

        try:
            entity = TradeEntity(
                id=str(uuid.uuid4()),
                symbol=trade.symbol,
                action=trade.action.value,
                quantity=trade.quantity,
                price=trade.price,
                timestamp=trade.timestamp
            )

            db.add(entity)
            db.commit()

        finally:
            db.close()

    def get_all_trades(self):
        db = SessionLocal()

        try:
            return db.query(TradeEntity).all()

        finally:
            db.close()