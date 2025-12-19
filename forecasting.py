from datetime import date
from typing import List, Tuple

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from app.models.inventory import SalesHistory


def load_sales_series(db: Session, medicine_id: int) -> pd.Series:
    rows: List[SalesHistory] = (
        db.query(SalesHistory)
        .filter(SalesHistory.medicine_id == medicine_id)
        .order_by(SalesHistory.date.asc())
        .all()
    )
    if not rows:
        return pd.Series(dtype=float)
    dates = [r.date for r in rows]
    qty = [r.quantity for r in rows]
    s = pd.Series(qty, index=pd.to_datetime(dates))
    daily = s.resample("D").sum().fillna(0)
    return daily


def naive_forecast(series: pd.Series, horizon_days: int = 30) -> List[Tuple[date, float]]:
    """Lightweight fallback forecast: use mean of last 30 days."""
    if series.empty:
        return []
    window = min(30, len(series))
    avg = float(series[-window:].mean())
    last_date = series.index.max().date()
    results: List[Tuple[date, float]] = []
    for i in range(1, horizon_days + 1):
        d = last_date + pd.Timedelta(days=i)
        results.append((d.date(), avg))
    return results


def safety_stock(series: pd.Series, service_factor: float = 1.65) -> float:
    """Simple safety stock using std dev of demand."""
    if len(series) < 2:
        return 0.0
    return float(series.std() * service_factor)




