# services/payment/app/utils.py
import random
import uuid
from .models import PaymentTransaction


async def simulate_payment(order_id: str, user_id: str, amount: float) -> PaymentTransaction:
    """
    Simulate a payment attempt.
    Randomly succeed or fail (80% success chance).
    """
    success = random.random() < 0.8  # 80% chance for success
    transaction_id = str(uuid.uuid4())

    status = "succeeded" if success else "failed"

    # create a payment transaction object (not yet saved)
    transaction = PaymentTransaction(
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        transaction_id=transaction_id,
        status=status,
    )

    # save to DB
    await transaction.insert()
    print(f"💳 Payment for order {order_id}: {status.upper()} (Transaction: {transaction_id})")

    return transaction
