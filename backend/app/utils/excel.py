from datetime import datetime
from typing import IO

import pandas as pd
from sqlalchemy.orm import Session

from app.models.inventory import Medicine, Supplier, StockBatch, SalesHistory


def normalize_column(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def process_inventory_excel(db: Session, file: IO[bytes]) -> None:
    df = pd.read_excel(file)
    df.columns = [normalize_column(c) for c in df.columns]

    required_cols = {"sku", "name", "batch_number", "quantity", "expiry_date"}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    for _, row in df.iterrows():
        sku = str(row["sku"])
        med = db.query(Medicine).filter(Medicine.sku == sku).first()
        if not med:
            med = Medicine(
                sku=sku,
                name=row.get("name"),
                category=row.get("category"),
                strength=row.get("strength"),
                form=row.get("form"),
            )
            db.add(med)
            db.flush()

        supplier_name = row.get("supplier")
        if supplier_name:
            supplier = (
                db.query(Supplier).filter(Supplier.name == supplier_name).first()
            )
            if not supplier:
                supplier = Supplier(name=supplier_name)
                db.add(supplier)
                db.flush()
            med.supplier = supplier

        expiry_val = row["expiry_date"]
        if isinstance(expiry_val, datetime):
            expiry_date = expiry_val.date()
        else:
            expiry_date = pd.to_datetime(expiry_val).date()

        quantity = int(row["quantity"])

        batch = StockBatch(
            medicine_id=med.id,
            batch_number=str(row["batch_number"]),
            quantity=quantity,
            remaining_quantity=quantity,
            expiry_date=expiry_date,
            received_date=datetime.utcnow().date(),
        )
        db.add(batch)

    db.commit()


def process_sales_excel(db: Session, file: IO[bytes]) -> None:
    df = pd.read_excel(file)
    df.columns = [normalize_column(c) for c in df.columns]
    required_cols = {"sku", "date", "quantity"}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    for _, row in df.iterrows():
        sku = str(row["sku"])
        med = db.query(Medicine).filter(Medicine.sku == sku).first()
        if not med:
            continue
        sale_date = pd.to_datetime(row["date"]).date()
        quantity = int(row["quantity"])
        sale = SalesHistory(
            medicine_id=med.id,
            date=sale_date,
            quantity=quantity,
        )
        db.add(sale)

    db.commit()




