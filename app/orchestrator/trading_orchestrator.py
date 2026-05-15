from app.risk.risk_manager import (
    RiskManager
)

from app.broker.trading_service import (
    TradingService
)

from app.models.paper_account import (
    PaperAccount
)
from app.market.market_data_provider import MarketDataProvider

from app.logging.agent_logger import AgentLogger
from app.memory.decision_log_repository import DecisionLogRepository

from app.skills.ai_stock_analysis_skill import AiStockAnalysisSkill


class TradingOrchestrator:
    DEFAULT_ORDER_QUANTITY = 1

    def __init__(self):
        self.market_data_provider = MarketDataProvider()
        self.skill = AiStockAnalysisSkill()
        self.risk_manager = RiskManager()
        self.trading_service = TradingService()
        self.logger = AgentLogger()
        self.decision_repository = DecisionLogRepository()

    def process_symbol(
        self,
        account: PaperAccount,
        symbol: str
    ) -> PaperAccount:
        try:
            stock_data = self.market_data_provider.get_stock_data(symbol)
        except Exception as e:
            self.logger.log(f"Market data unavailable for {symbol}: {e}")
            self._save_decision(
                symbol=symbol,
                signal_action="HOLD",
                signal_confidence=0.0,
                signal_reason=f"Market data unavailable. Error: {e}",
                risk_approved=False,
                risk_reason="Trade skipped because market data could not be fetched",
                final_action="SKIP",
                quantity=0,
                price=0
            )
            return account

        signal = self.skill.analyze(stock_data)
        order_price = stock_data.current_price

        self.logger.log(
            f"Signal for {symbol}: {signal.action} "
            f"at {order_price}"
        )

        if signal.action != "BUY":
            self._save_decision(
                symbol=symbol,
                signal_action=signal.action,
                signal_confidence=signal.confidence,
                signal_reason=signal.reason,
                risk_approved=False,
                risk_reason="Trade skipped because signal was not BUY",
                final_action="SKIP",
                quantity=0,
                price=order_price
            )
            return account

        risk_decision = self.risk_manager.can_buy(
            account=account,
            symbol=symbol,
            quantity=self.DEFAULT_ORDER_QUANTITY,
            price=order_price
        )

        self.logger.log(f"Risk decision: {risk_decision.reason}")

        if not risk_decision.approved:
            self._save_decision(
                symbol=symbol,
                signal_action=signal.action,
                signal_confidence=signal.confidence,
                signal_reason=signal.reason,
                risk_approved=False,
                risk_reason=risk_decision.reason,
                final_action="REJECT",
                quantity=self.DEFAULT_ORDER_QUANTITY,
                price=order_price
            )
            return account

        self.logger.log(f"Executing BUY for {symbol} at {order_price}")

        updated_account = self.trading_service.buy(
            account=account,
            symbol=symbol,
            quantity=self.DEFAULT_ORDER_QUANTITY,
            price=order_price
        )

        self._save_decision(
            symbol=symbol,
            signal_action=signal.action,
            signal_confidence=signal.confidence,
            signal_reason=signal.reason,
            risk_approved=True,
            risk_reason=risk_decision.reason,
            final_action="BUY",
            quantity=self.DEFAULT_ORDER_QUANTITY,
            price=order_price
        )

        return updated_account

    def _save_decision(
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
        self.decision_repository.save_decision(
            symbol=symbol,
            signal_action=signal_action,
            signal_confidence=signal_confidence,
            signal_reason=signal_reason,
            risk_approved=risk_approved,
            risk_reason=risk_reason,
            final_action=final_action,
            quantity=quantity,
            price=price
        )
