from abc import ABC
from abc import abstractmethod

from pytheater.actor_system import ActorSystem


class Actor(ABC):

    def __init__(self, system=None):
        self.system: ActorSystem = system

    @abstractmethod
    def receive(self, message, state=None):
        pass
