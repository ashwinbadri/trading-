import uuid
from datetime import datetime

from app.memory.database import SessionLocal
from app.memory.db_models import AgentLogEntity


class AgentLogRepository:

    def save_log(self, message: str):
        db = SessionLocal()

        try:
            entity = AgentLogEntity(
                id=str(uuid.uuid4()),
                message=message,
                timestamp=datetime.now()
            )

            db.add(entity)
            db.commit()

        finally:
            db.close()

    def get_all_logs(self):
        db = SessionLocal()

        try:
            return db.query(AgentLogEntity).all()

        finally:
            db.close()