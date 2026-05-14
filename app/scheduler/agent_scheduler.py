from apscheduler.schedulers.background import BackgroundScheduler

from app.models.paper_account import PaperAccount
from app.orchestrator.trading_orchestrator import TradingOrchestrator

account = PaperAccount(
    cash_balance=10_000,
    positions=[],
    trades=[]
)

orchestrator = TradingOrchestrator()

watchlist = ["AAPL", "TSLA", "NVDA"]


def run_agent_once():
    global account

    print("\nRunning scheduled agent loop...")

    for symbol in watchlist:
        account = orchestrator.process_symbol(
            account=account,
            symbol=symbol
        )

    print("\nCurrent Portfolio:")
    print(account)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agent_once, "interval", seconds=30)
    scheduler.start()

    print("Scheduler started")
