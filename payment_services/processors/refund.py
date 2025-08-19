from typing import Protocol
from commons import PaymentResponse

class RefundPaymentProtocol(Protocol):
    def process_refund(self, transaction_id:str) -> PaymentResponse: ...