from app.risk.risk_manager import (
    RiskManager
)

from app.broker.trading_service import (
    TradingService
)

from app.models.paper_account import (
    PaperAccount
)

from app.logging.agent_logger import AgentLogger

from app.skills.ai_stock_analysis_skill import AiStockAnalysisSkill

class TradingOrchestrator:

    def __init__(self):

        self.skill = AiStockAnalysisSkill()
        self.risk_manager = RiskManager()

        self.trading_service = TradingService()

        self.logger = AgentLogger()

    def process_symbol(
        self,
        account: PaperAccount,
        symbol: str
    ) -> PaperAccount:

        signal = self.skill.analyze(symbol)

        self.logger.log(f"Signal for {symbol}: {signal.action}")

        if signal.action != "BUY":
            return account

        risk_decision = self.risk_manager.can_buy(
            account=account,
            symbol=symbol,
            quantity=1,
            price=100
        )

        self.logger.log(f"Risk decision: {risk_decision.reason}")

        if not risk_decision.approved:
            return account

        self.logger.log(f"Executing BUY for {symbol}")

        updated_account = self.trading_service.buy(
            account=account,
            symbol=symbol,
            quantity=1,
            price=100
        )

        return updated_account