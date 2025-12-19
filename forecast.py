from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.forecast_service import forecast_medicine, forecast_all_medicines


router = APIRouter(prefix="/forecast", tags=["forecast"])


class Point(BaseModel):
    date: str
    quantity: float


class ForecastOut(BaseModel):
    history: List[Point]
    forecast: List[Point]
    safety_stock: float
    reorder_quantity: int
    current_stock: int


@router.get("/medicine/{medicine_id}", response_model=ForecastOut)
def get_medicine_forecast(medicine_id: int, db: Session = Depends(get_db)):
    data: Dict = forecast_medicine(db, medicine_id)
    return data


@router.get("/overview")
def forecast_overview(db: Session = Depends(get_db)):
    return forecast_all_medicines(db)




