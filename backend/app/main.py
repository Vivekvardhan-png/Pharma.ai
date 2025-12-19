from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import inventory, upload, alerts, forecast, chatbot
from app.models.base import Base, engine
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.services.inventory_service import scan_expiry_alerts, scan_stock_alerts


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pharmacy AI Inventory Platform",
        version="1.0.0",
    )

    # CORS for frontend (adjust in production)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(inventory.router)
    app.include_router(upload.router)
    app.include_router(alerts.router)
    app.include_router(forecast.router)
    app.include_router(chatbot.router)

    # Scheduler for background jobs
    scheduler = BackgroundScheduler()

    def scheduled_expiry_scan() -> None:
        db: Session = SessionLocal()
        try:
            scan_expiry_alerts(db)
        finally:
            db.close()

    def scheduled_stock_scan() -> None:
        db: Session = SessionLocal()
        try:
            scan_stock_alerts(db)
        finally:
            db.close()

    scheduler.add_job(scheduled_expiry_scan, "interval", hours=12, id="expiry_scan")
    scheduler.add_job(scheduled_stock_scan, "interval", hours=6, id="stock_scan")
    scheduler.start()

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()


