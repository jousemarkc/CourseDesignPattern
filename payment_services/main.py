from notifier import EmailNotifier, NotifierProtocol, SMSNotifier
from services import PaymentService
from loggers import TransactionLogger
from validators import CustomerValidator, PaymentDataValidator
from commons import CustomerData, ContactInfo, PaymentData
from logging_service import PaymentServiceLogging


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
    customer_data = CustomerData(name="Jhon Deive", contact_info=contact_info)
    return customer_data

if __name__ == '__main__':
    customer_data = get_customer_data()
    notifier = get_notifier_implementation(customer_data=customer_data)
    customer_validator = CustomerValidator()
    payment_data_validator = PaymentDataValidator()
    logger = TransactionLogger()
    payment_data = PaymentData(amount=512, source='tok_mastercard', currency='USD')

    service = PaymentService.create_with_payment_processor(
        payment_data=payment_data,
        notifier=notifier,
        customer_validator=customer_validator,
        payment_validator=payment_data_validator,
        logger=logger
    )

    process_service = service.process_transaction(customer_data=customer_data, payment_data=payment_data)

    logging_service = PaymentServiceLogging(wrapped=service)
    logging_service.process_refund(transaction_id=process_service.transaction_id)