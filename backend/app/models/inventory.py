from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship

from .base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)

    medicines = relationship("Medicine", back_populates="supplier")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    ai_category = Column(String, index=True, nullable=True)
    strength = Column(String, nullable=True)
    form = Column(String, nullable=True)  # tablet, syrup, etc.
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    # simple stock policies; can be tuned per SKU
    min_stock = Column(Integer, nullable=True)  # low-stock threshold
    max_stock = Column(Integer, nullable=True)  # overstock threshold

    supplier = relationship("Supplier", back_populates="medicines")
    batches = relationship("StockBatch", back_populates="medicine")
    sales = relationship("SalesHistory", back_populates="medicine")


class StockBatch(Base):
    __tablename__ = "stock_batches"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_number = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    remaining_quantity = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    received_date = Column(Date, nullable=False, default=date.today)

    medicine = relationship("Medicine", back_populates="batches")


class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)

    medicine = relationship("Medicine", back_populates="sales")


class ExpiredDamagedStock(Base):
    __tablename__ = "expired_damaged_stock"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("stock_batches.id"), nullable=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)  # expired, damaged, recalled
    cost = Column(Float, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # low_stock, expiry, overstock, reorder
    priority = Column(String, nullable=False)  # critical, warning, info
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)


