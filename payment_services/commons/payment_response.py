from pydantic import BaseModel
from typing import Optional

class PaymentResponse(BaseModel):
    status: str
    amount: int
    transaction_id: Optional[str] = None
    message: Optional[str] = None