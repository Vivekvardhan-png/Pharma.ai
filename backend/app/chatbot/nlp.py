from typing import Dict

from sqlalchemy.orm import Session

from app.models.inventory import Medicine, StockBatch, ExpiredDamagedStock
from app.services.forecast_service import forecast_all_medicines
from app.services.inventory_service import calculate_stock_levels


def handle_query(db: Session, query: str) -> Dict:
    """Lightweight rule-based NLP with simple keyword matching.

    This is intentionally minimal but structured so a spaCy / HF model
    can be plugged in later without changing the API surface.
    """
    q = query.lower()

    if "how many" in q or "left" in q:
        # e.g. "How many Paracetamol are left?"
        for med in db.query(Medicine).all():
            if med.name.lower() in q:
                qty = calculate_stock_levels(db, med.id)
                return {
                    "type": "stock_lookup",
                    "medicine": med.name,
                    "quantity": qty,
                    "text": f"There are {qty} units of {med.name} in stock.",
                }

    if "expire this week" in q or "expire this month" in q or "which medicines expire" in q:
        from datetime import date, timedelta

        today = date.today()
        horizon = 7 if "week" in q else 30
        cutoff = today + timedelta(days=horizon)
        batches = (
            db.query(StockBatch)
            .filter(
                StockBatch.expiry_date >= today,
                StockBatch.expiry_date <= cutoff,
                StockBatch.remaining_quantity > 0,
            )
            .all()
        )
        items = [
            {
                "medicine": b.medicine.name,
                "batch": b.batch_number,
                "expiry_date": b.expiry_date.isoformat(),
                "quantity": b.remaining_quantity,
            }
            for b in batches
        ]
        return {
            "type": "expiry_list",
            "items": items,
            "text": f"{len(items)} batches expiring in the next {horizon} days.",
        }

    if "wastage" in q or "expired stock" in q or "generate wastage report" in q:
        items = db.query(ExpiredDamagedStock).all()
        total_cost = float(sum(i.cost or 0 for i in items))
        return {
            "type": "wastage_report",
            "total_cost": total_cost,
            "count": len(items),
            "text": f"Total wastage cost is {total_cost:.2f} across {len(items)} records.",
        }

    if "reorder" in q or "suggest reorder list" in q:
        overview = forecast_all_medicines(db)
        suggestions = [
            {
                "medicine_id": item["medicine_id"],
                "name": item["name"],
                "reorder_quantity": item["reorder_quantity"],
            }
            for item in overview
            if item["reorder_quantity"] > 0
        ]
        return {
            "type": "reorder_suggestions",
            "items": suggestions,
            "text": f"{len(suggestions)} medicines need reordering.",
        }

    return {
        "type": "fallback",
        "text": "I did not understand that query. Try asking about stock, expiry, wastage, or reorder suggestions.",
    }



