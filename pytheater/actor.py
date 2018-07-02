from abc import ABC
from abc import abstractmethod

from asyncio.queues import Queue

from actor_system import ActorSystem


class Actor(ABC):

    def __init__(self, system=None):
        self.system: ActorSystem = system
        self.inbox: Queue = Queue(maxsize=10, loop=system.loop)

    async def new_message(self, message):
        await self.inbox.put(message)

    def tell(self, message):
        print(f"Telling message {message}")
        self.system.schedule(self.new_message(message))

    @abstractmethod
    def receive(self, message):
        pass

    async def run(self):
        while True:
            message = await self.inbox.get()

            #  signal to take the actor out of scene
            if message is None:
                break

            self.receive(message)



