from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderCreatedEvent(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    status: str = "created"