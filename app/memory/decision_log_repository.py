import uuid
from datetime import datetime

from sqlalchemy import desc

from app.memory.database import SessionLocal
from app.memory.db_models import DecisionLogEntity


class DecisionLogRepository:

    def save_decision(
        self,
        symbol: str,
        signal_action: str,
        signal_confidence: float,
        signal_reason: str,
        risk_approved: bool,
        risk_reason: str,
        final_action: str,
        quantity: float,
        price: float
    ):
        db = SessionLocal()

        try:
            entity = DecisionLogEntity(
                id=str(uuid.uuid4()),
                symbol=symbol.upper(),
                signal_action=signal_action,
                signal_confidence=signal_confidence,
                signal_reason=signal_reason,
                risk_approved="YES" if risk_approved else "NO",
                risk_reason=risk_reason,
                final_action=final_action,
                quantity=quantity,
                price=price,
                timestamp=datetime.now()
            )

            db.add(entity)
            db.commit()

        finally:
            db.close()

    def get_all_decisions(self):
        db = SessionLocal()

        try:
            return db.query(DecisionLogEntity).order_by(
                desc(DecisionLogEntity.timestamp)
            ).all()

        finally:
            db.close()
