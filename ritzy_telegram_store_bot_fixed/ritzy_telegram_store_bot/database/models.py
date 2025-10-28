from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class UserModel(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    email: Optional[str] = None
    balance_usd: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    status: str = "PAID"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TransactionModel(BaseModel):
    telegram_id: int
    type: str  # DEPOSIT / WITHDRAWAL / ADJUSTMENT
    amount_usd: float
    fee_usd: float = 0.0
    cashback_usd: float = 0.0
    tx_ref: Optional[str] = None
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InvoiceModel(BaseModel):
    invoice_id: str
    telegram_id: int
    amount_usd: float
    payment_methods: Optional[list[str]] = None
    status: str = "NEW"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
