from typing import Protocol
from services_protocol import PaymentServiceProtocol
from commons import CustomerData, PaymentData, PaymentResponse


class PaymentServiceDecoratorPotocol(Protocol):
    wrapped: PaymentServiceProtocol

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        ...

    def process_refund(self, transaction_id: str):
        ...

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        ...