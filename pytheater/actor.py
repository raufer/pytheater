from abc import ABC
from abc import abstractmethod

from actor_address import ActorAddress


class Actor(ABC):

    def __init__(self, system=None, uuid=None):
        self.system: 'ActorSystem' = system
        self.uuid = uuid
        self.state = None

    def constructor(self) -> None:
        self.state = {}

    @abstractmethod
    def receive(self, message, sender: ActorAddress):
        pass

    def next_state(self, new_state) -> None:
        self.system.store.put(self.uuid, self.state, new_state)
