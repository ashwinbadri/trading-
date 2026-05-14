from fastapi import FastAPI

from app.api.trading_api import (
    router as trading_router
)

from app.scheduler.agent_scheduler import (
    start_scheduler
)


app = FastAPI()

app.include_router(trading_router)


@app.on_event("startup")
def startup_event():
    start_scheduler()
