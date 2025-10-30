from typing import List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product_id: str = Field(..., description="Item ID")
    quantity: int = Field(..., gt=0, description="quantity")
    price: float = Field(..., ge=0, description="price")


class Order(Document):
    """
    Represent order in the DB
    """
    order_id: str = Field(..., index=True, unique=True)
    user_id: str
    items: List[OrderItem]
    total: float = 0.0
    status: str = "created"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


    class Settings:
        name = "orders"  # Collection name in Mongo