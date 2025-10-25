from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class UserModel(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    balance_usd: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CategoryModel(BaseModel):
    name: str
    emoji: Optional[str] = None

class ProductModel(BaseModel):
    name: str
    category: str
    price_usd: float
    description: Optional[str] = None
    image_url: Optional[str] = None
    active: bool = True

class OrderModel(BaseModel):
    order_id: str
    telegram_id: int
    product_name: str
    amount_usd: float
    status: str = "PAID"  # PAID / REFUNDED / CANCELLED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransactionModel(BaseModel):
    telegram_id: int
    type: str  # DEPOSIT / WITHDRAWAL / ADJUSTMENT
    amount_usd: float
    fee_usd: float = 0.0
    cashback_usd: float = 0.0
    tx_ref: Optional[str] = None   # invoice id or hash
    status: str = "PENDING"        # PENDING / CONFIRMED / FAILED
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InvoiceModel(BaseModel):
    invoice_id: str
    telegram_id: int
    amount_usd: float
    payment_methods: Optional[list[str]] = None
    status: str = "NEW"
    created_at: datetime = Field(default_factory=datetime.utcnow)
