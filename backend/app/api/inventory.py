from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.inventory import Medicine, StockBatch, Supplier
from app.services.inventory_service import (
    calculate_stock_levels,
    get_fefo_batches,
)


router = APIRouter(prefix="/inventory", tags=["inventory"])


class SupplierOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MedicineOut(BaseModel):
    id: int
    name: str
    sku: str
    category: Optional[str]
    ai_category: Optional[str]
    strength: Optional[str]
    form: Optional[str]
    supplier: Optional[SupplierOut]
    total_stock: int

    class Config:
        orm_mode = True


class BatchOut(BaseModel):
    id: int
    batch_number: str
    quantity: int
    remaining_quantity: int
    expiry_date: str

    class Config:
        orm_mode = True


@router.get("/medicines", response_model=List[MedicineOut])
def list_medicines(db: Session = Depends(get_db)):
    medicines = db.query(Medicine).all()
    result: List[MedicineOut] = []
    for m in medicines:
        total_stock = calculate_stock_levels(db, m.id)
        result.append(
            MedicineOut(
                id=m.id,
                name=m.name,
                sku=m.sku,
                category=m.category,
                ai_category=m.ai_category,
                strength=m.strength,
                form=m.form,
                supplier=m.supplier,
                total_stock=total_stock,
            )
        )
    return result


@router.get("/medicines/{medicine_id}/batches", response_model=List[BatchOut])
def list_batches(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    batches = get_fefo_batches(db, medicine_id)
    return batches




