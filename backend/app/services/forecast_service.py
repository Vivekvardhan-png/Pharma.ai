from datetime import date
from typing import Dict, List

from sqlalchemy.orm import Session

from app.ml.forecasting import load_sales_series, naive_forecast, safety_stock
from app.models.inventory import Medicine
from app.services.inventory_service import calculate_stock_levels


def forecast_medicine(db: Session, medicine_id: int, horizon_days: int = 30) -> Dict:
    series = load_sales_series(db, medicine_id)
    forecast_points = naive_forecast(series, horizon_days=horizon_days)
    safety = safety_stock(series)
    total_stock = calculate_stock_levels(db, medicine_id)

    daily_demand = (
        float(series[-30:].mean()) if len(series) > 0 else 0.0
    )
    reorder_quantity = max(int(daily_demand * horizon_days + safety - total_stock), 0)

    return {
        "history": [
            {"date": d.strftime("%Y-%m-%d"), "quantity": float(series[d])}
            for d in series.index
        ],
        "forecast": [
            {"date": d.strftime("%Y-%m-%d"), "quantity": q}
            for d, q in forecast_points
        ],
        "safety_stock": safety,
        "reorder_quantity": reorder_quantity,
        "current_stock": total_stock,
    }


def forecast_all_medicines(db: Session, horizon_days: int = 30) -> List[Dict]:
    meds: List[Medicine] = db.query(Medicine).all()
    results: List[Dict] = []
    for m in meds:
        f = forecast_medicine(db, m.id, horizon_days=horizon_days)
        f["medicine_id"] = m.id
        f["name"] = m.name
        results.append(f)
    return results



