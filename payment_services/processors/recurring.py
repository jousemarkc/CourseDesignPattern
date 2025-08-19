from typing import Protocol
from commons import CustomerData, PaymentData, PaymentResponse

class RecurringPaymentProtocol(Protocol):
        def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) ->PaymentResponse: ...