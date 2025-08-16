from typing import Protocol
from commons import PaymentResponse

class RefundPaymentProtocol(Protocol):
    def refund_payment(self, transaction_id:str) -> PaymentResponse: ...