from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.utils.excel import process_inventory_excel, process_sales_excel


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/inventory")
async def upload_inventory(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files are supported")
    try:
        process_inventory_excel(db, file.file)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok"}


@router.post("/sales")
async def upload_sales(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files are supported")
    try:
        process_sales_excel(db, file.file)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok"}




