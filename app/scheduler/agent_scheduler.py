from apscheduler.schedulers.background import BackgroundScheduler

from app.memory.account_repository import AccountRepository
from app.orchestrator.trading_orchestrator import TradingOrchestrator

orchestrator = TradingOrchestrator()
account_repository = AccountRepository()

watchlist = ["AAPL", "TSLA", "NVDA"]


def run_agent_once():
    account = account_repository.get_account()

    print("\nRunning scheduled agent loop...")

    for symbol in watchlist:
        account = orchestrator.process_symbol(
            account=account,
            symbol=symbol
        )

    account_repository.save_account(account)

    print("\nCurrent Portfolio:")
    print(account)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agent_once, "interval", seconds=30)
    scheduler.start()

    print("Scheduler started")
