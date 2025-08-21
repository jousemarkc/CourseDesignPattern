from notifier import EmailNotifier, NotifierProtocol, SMSNotifier
from commons import CustomerData, ContactInfo, PaymentData
from logging_service import PaymentServiceLogging
from builder import PaymentServiceBuilder


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

    payment_data = PaymentData(amount=444, source='tok_mastercard', currency='USD')

    builder = PaymentServiceBuilder()

    service = builder.set_logger().set_payment_validator().set_customer_validator().set_payment_processor(payment_data).set_notifier(customer_data).set_listeners().build()

    process_service = service.process_transaction(customer_data=customer_data, payment_data=payment_data)
