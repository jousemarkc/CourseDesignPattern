from dataclasses import dataclass
from typing import Optional, Self
from processors import PaymentProcessorProtocol
from notifier import NotifierProtocol, EmailNotifier, SMSNotifier
from validators import ChainHandler, CustomerHandler, PaymentHandler
from loggers import TransactionLogger
from commons import PaymentData, CustomerData
from factory import PaymentProcessorFactory
from services import PaymentService
from listeners import ListenersManager, AccountabilityListener


@dataclass
class PaymentServiceBuilder:
    payment_processor: Optional[PaymentProcessorProtocol] = None
    notifier: Optional[NotifierProtocol] = None
    validator : Optional[ChainHandler] = None
    logger: Optional[TransactionLogger] = None
    listener: Optional[ListenersManager] = None

    def set_logger(self) -> Self:
        self.logger = TransactionLogger()
        return self
    
    
    def set_payment_processor(self, payment_data: PaymentData) -> Self:
        self.payment_processor = PaymentProcessorFactory.create_payment_processor(payment_data)
        return self
    
    def set_chain_of_validations(self) -> Self:
        customer_handler = CustomerHandler()
        payment_handler = PaymentHandler()
        customer_handler.set_next(payment_handler)
        self.validator = customer_handler
        return self
    
    def set_notifier(self, customer_data: CustomerData) -> Self:
        if customer_data.contact_info.email:
            self.notifier = EmailNotifier()
            return self
        elif customer_data.contact_info.phone:
            self.notifier = SMSNotifier(gateway='MyCustomGateway')
            return self
        else:
            raise ValueError('Can not select notifier class.')

    def set_listeners(self) -> Self:
        listener = ListenersManager()
        acountability_listener = AccountabilityListener()
        listener.subscribe(acountability_listener)
        self.listener = listener
        return self

    def build(self):
        if not all([
            self.payment_processor,
            self.notifier,
            self.validator,
            self.logger,
            self.listener
        ]):
            missing = [
                name 
                for name, value in [
                    ('payment_processor', self.payment_processor),
                    ('notifier', self.notifier),
                    ('validator', self.validator),
                    ('logger', self.logger),
                    ('listener', self.listener)
                ]
                if value is None
            ]
            raise ValueError(f'Missing dependencies: {missing}')
        return PaymentService(
            payment_processor=self.payment_processor,
            notifier=self.notifier,
            validators=self.validator,
            logger=self.logger,
            listeners=self.listener
        )