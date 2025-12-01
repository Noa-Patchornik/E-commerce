from beanie import Document
from datetime import datetime
from pydantic import Field

class PaymentTransaction(Document):
    order_id: str
    user_id: str
    amount: float
    status: str = Field(default="pending")
    transaction_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "payments"

    class Config:
        arbitrary_types_allowed = True
