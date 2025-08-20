from typing import Protocol
from typing import Optional
from processors import PaymentProcessorProtocol, RefundPaymentProtocol, RecurringPaymentProtocol
from notifier import NotifierProtocol
from validators import CustomerValidator, PaymentDataValidator
from loggers import TransactionLogger
from commons import CustomerData, PaymentData, PaymentResponse
from listeners import ListenersManager



class PaymentServiceProtocol(Protocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    customer_validator: CustomerValidator 
    payment_validator: PaymentDataValidator 
    logger: TransactionLogger
    listeners: ListenersManager
    refund_processor: Optional[RefundPaymentProtocol] = None
    recurring_processor: Optional[RecurringPaymentProtocol] = None

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