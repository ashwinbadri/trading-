from fastapi import FastAPI

from app.api.trading_api import (
    router as trading_router
)
from app.memory.database import initialize_database

from app.scheduler.agent_scheduler import (
    start_scheduler
)


app = FastAPI()

app.include_router(trading_router)


@app.on_event("startup")
def startup_event():
    initialize_database()
    start_scheduler()
