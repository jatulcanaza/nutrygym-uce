from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.web import router as web_router
from app.core.mqtt_bridge import start_mqtt_bridge, stop_mqtt_bridge

app = FastAPI(
    title="Notification Dashboard Service",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(web_router)

@app.on_event("startup")
async def on_startup():
    start_mqtt_bridge()

@app.on_event("shutdown")
async def on_shutdown():
    stop_mqtt_bridge()
