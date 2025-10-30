from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]


class OrderCreatedEvent(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    status: str = "created"