from typing import List
from dataclasses import dataclass, field
from .listener import Listener


@dataclass
class ListenersManager[T]:
    listeners : List[Listener] = field(default_factory=list)

    def subscribe(self, listener: Listener) -> None:
        self.listeners.append(listener)

    def unsubscribe(self, listener: Listener) -> None:
        self.listeners.remove(listener)

    def notifyAll(self, event: T):
        for listener in self.listeners:
            listener.notify(event)