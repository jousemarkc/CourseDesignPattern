from dataclasses import dataclass
from typing import Optional, Self
from processors import PaymentProcessorProtocol, RefundPaymentProtocol, RecurringPaymentProtocol
from notifier import NotifierProtocol
from loggers import TransactionLogger
from commons import CustomerData, PaymentData, PaymentResponse, Request
from factory import PaymentProcessorFactory
from services_protocol import PaymentServiceProtocol
from listeners import ListenersManager
from validators import ChainHandler


@dataclass
class PaymentService(PaymentServiceProtocol):
    payment_processor: PaymentProcessorProtocol
    notifier: NotifierProtocol
    validators: ChainHandler
    logger: TransactionLogger
    listeners: ListenersManager
    refund_processor: Optional[RefundPaymentProtocol] = None
    recurring_processor: Optional[RecurringPaymentProtocol] = None

    @classmethod
    def create_with_payment_processor(cls, payment_data: PaymentData, **kwargs) -> Self:
        try:
            processor = PaymentProcessorFactory.create_payment_processor(payment_data)
            return processor
        except ValueError as e:
            print('Error creating class.')
            raise e


    # Method that let us to change strategy to the notifier
    def set_notifier(self, notifier: NotifierProtocol):
        print("Changing the notifier implementation")
        self.notifier = notifier

    def process_transaction(
        self, customer_data: CustomerData, payment_data: PaymentData
    ) -> PaymentResponse:
        try:
            request = Request(customer_data=customer_data, payment_data=payment_data)
            self.validators.handle(request=request)
        except Exception as e:
            print(f'Validations failed {e}')
            raise e
        payment_response = self.payment_processor.process_transaction(
            customer_data, payment_data
        )
        if payment_response.status == 'succeeded':
            self.listeners.notifyAll(f'Successful Payment to event: {payment_response.transaction_id}')
        else:
            self.listeners.notifyAll(f'Payment failed: {payment_response.transaction_id}')
        self.notifier.send_confirmation(customer_data)
        self.logger.log_transaction(
            customer_data, payment_data, payment_response
        )
        return payment_response

    def process_refund(self, transaction_id: str):
        if not self.refund_processor:
            raise Exception("This processor does not support refund")
        refund_response = self.refund_processor.refund_payment(transaction_id)
        self.logger.log_refund(transaction_id, refund_response)
        return refund_response

    def setup_recurring(
        self, customer_data: CustomerData, payment_data: PaymentData
    ):
        if not self.recurring_processor:
            raise Exception("This processor does not support recurring")
        recurring_response = self.recurring_processor.setup_recurring_payment(
            customer_data, payment_data
        )
        self.logger.log_transaction(
            customer_data, payment_data, recurring_response
        )
        return recurring_response