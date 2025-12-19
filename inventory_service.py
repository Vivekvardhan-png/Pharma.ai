from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.inventory import Medicine, StockBatch, SalesHistory, Alert


EXPIRY_THRESHOLDS = [30, 15, 7]


def get_medicine_by_sku(db: Session, sku: str) -> Optional[Medicine]:
    return db.query(Medicine).filter(Medicine.sku == sku).first()


def calculate_stock_levels(db: Session, medicine_id: int) -> int:
    total = (
        db.query(func.sum(StockBatch.remaining_quantity))
        .filter(StockBatch.medicine_id == medicine_id)
        .scalar()
    )
    return int(total or 0)


def get_fefo_batches(db: Session, medicine_id: int) -> List[StockBatch]:
    return (
        db.query(StockBatch)
        .filter(
            StockBatch.medicine_id == medicine_id,
            StockBatch.remaining_quantity > 0,
        )
        .order_by(StockBatch.expiry_date.asc())
        .all()
    )


def consume_stock_fefo(db: Session, medicine_id: int, quantity: int) -> int:
    """Apply FEFO: consume from earliest-expiry batches first. Returns consumed."""
    remaining = quantity
    batches = get_fefo_batches(db, medicine_id)
    for batch in batches:
        if remaining <= 0:
            break
        take = min(batch.remaining_quantity, remaining)
        batch.remaining_quantity -= take
        remaining -= take
    db.commit()
    return quantity - remaining


def scan_expiry_alerts(db: Session) -> None:
    today = date.today()
    for days in EXPIRY_THRESHOLDS:
        threshold_date = today + timedelta(days=days)
        batches = (
            db.query(StockBatch)
            .filter(
                StockBatch.expiry_date <= threshold_date,
                StockBatch.expiry_date >= today,
                StockBatch.remaining_quantity > 0,
            )
            .all()
        )
        for batch in batches:
            medicine = batch.medicine
            message = (
                f"{medicine.name} (batch {batch.batch_number}) "
                f"expires in <= {days} days on {batch.expiry_date}"
            )
            alert = Alert(
                type="expiry",
                priority="critical" if days <= 7 else "warning",
                message=message,
            )
            db.add(alert)
    db.commit()


def scan_stock_alerts(db: Session) -> None:
    """Generate low-stock and overstock alerts based on per-medicine thresholds."""
    medicines = db.query(Medicine).all()
    for med in medicines:
        total = calculate_stock_levels(db, med.id)
        # Low stock
        if med.min_stock is not None and total <= med.min_stock:
            msg = (
                f"Low stock for {med.name} (SKU {med.sku}): "
                f"{total} units remaining (threshold {med.min_stock})."
            )
            alert = Alert(type="low_stock", priority="warning", message=msg)
            db.add(alert)
        # Overstock
        if med.max_stock is not None and total >= med.max_stock:
            msg = (
                f"Overstock for {med.name} (SKU {med.sku}): "
                f"{total} units (threshold {med.max_stock})."
            )
            alert = Alert(type="overstock", priority="info", message=msg)
            db.add(alert)
    db.commit()



