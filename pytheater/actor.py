from abc import ABC
from abc import abstractmethod

from actor_address import ActorAddress

from typing import Any


class Actor(ABC):

    def __init__(self, system=None, uuid=None):
        self.system: 'ActorSystem' = system
        self.uuid = uuid
        self.state = None

    def constructor(self, *args, **kwargs) -> None:
        self.state = {}

    @abstractmethod
    def receive(self, message: Any, sender: ActorAddress):
        pass

    def next_state(self, new_state) -> None:
        self.system.store.put(self.uuid, self.state, new_state)

    def __repr__(self):
        return f"Actor [{self.__class__}]"
