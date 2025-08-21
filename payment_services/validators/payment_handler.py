from .chain_handler import ChainHandler
from commons import Request
from .payment import PaymentDataValidator


class PaymentHandler(ChainHandler):
    def handle(self, request: Request):
        validator = PaymentDataValidator()
        try:
            validator.validate(request.payment_data)
            if self._nex_handler:
                self._nex_handler.handle(request)
        except Exception as e:
            print('error')
            raise e 