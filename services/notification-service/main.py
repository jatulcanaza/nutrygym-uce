from fastapi import FastAPI
from threading import Thread

from app.routes.health import router as health_router
from app.core.logger import get_logger
from app.core.rabbitmq import start_consumer_forever

log = get_logger("main")

app = FastAPI(title="Notification Service")

app.include_router(health_router)

@app.on_event("startup")
def startup():
    t = Thread(target=start_consumer_forever, daemon=True)
    t.start()
    log.info("Notification Service started (RabbitMQ consumer thread running).")
