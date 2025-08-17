from .services import PaymentService
from .processors import StripePaymentProcessor
from .notifier import EmailNotifier, NotifierProtocol, SMSNotifier
from .loggers import TransactionLogger
from validators import CustomerValidator, PaymentDataValidator
from .commons import CustomerData, ContactInfo


def get_email_notifier() -> EmailNotifier:
    return EmailNotifier()


def get_sms_notifier() -> SMSNotifier:
    return SMSNotifier(gateway="SMSGatewayExample")


def get_notifier_implementation(customer_data: CustomerData) -> NotifierProtocol:
    
    if customer_data.contact_info.phone:
        return get_sms_notifier()
    elif customer_data.contact_info.email:
        return get_email_notifier()
    else:
        raise ValueError("Can not choose the correct strategy")


def get_customer_data() -> CustomerData:
    contact_info = ContactInfo(email="jhon@deive.com")
    customer_data = CustomerData(name="Jhon Deive")
    return customer_data

if __name__ == '__main__':
    stripe_payment_processor = StripePaymentProcessor()
    customer_data = get_customer_data()
    notifier = get_notifier_implementation(customer_data=customer_data)
    email_notifier = get_email_notifier()
    sms_notifier = get_sms_notifier()
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()
    service = PaymentService(
        payment_processor=stripe_payment_processor,
        notifier=notifier,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
        logger=logger
    )
    #Changing notifier strategy to email
    service.set_notifier(email_notifier)
    #Changing notifier strategy to sms
    service.set_notifier(sms_notifier)