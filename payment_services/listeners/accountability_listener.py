from .listener import Listener


class AccountabilityListener[T](Listener):
    def notify(self, event: T):
        print(f'Notifying the accounting system about event: {event}')