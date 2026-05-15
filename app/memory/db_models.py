from sqlalchemy import Column, Float, String, DateTime
from app.memory.database import Base


class PaperAccountEntity(Base):
    __tablename__ = "paper_account"

    id = Column(String, primary_key=True, index=True)
    cash_balance = Column(Float, nullable=False)


class TradeEntity(Base):
    __tablename__ = "trades"

    id = Column(String, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    action = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class PositionEntity(Base):
    __tablename__ = "positions"

    symbol = Column(String, primary_key=True, index=True)
    quantity = Column(Float, nullable=False)
    average_price = Column(Float, nullable=False)


class AgentLogEntity(Base):
    __tablename__ = "agent_logs"

    id = Column(String, primary_key=True, index=True)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


class DecisionLogEntity(Base):
    __tablename__ = "decision_logs"

    id = Column(String, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    signal_action = Column(String, nullable=False)
    signal_confidence = Column(Float, nullable=False)
    signal_reason = Column(String, nullable=False)
    risk_approved = Column(String, nullable=False)
    risk_reason = Column(String, nullable=False)
    final_action = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
