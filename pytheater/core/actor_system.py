import asyncio
import threading

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future
from asyncio.queues import Queue

from pytheater.core import SystemEventLoop
from pytheater.actor_address import ActorAddress
from pytheater.core.store import Store
from pytheater.utils.identifier import gen_uuid


class ActorSystem(SystemEventLoop):

    def __init__(self):
        self.performing = []
        self.store = Store()
        super(ActorSystem, self).__init__()

    def create_actor(self, actor_class) -> ActorAddress:
        uuid = gen_uuid()
        actor = actor_class(system=self, uuid=uuid)
        actor.constructor()

        mailbox = create_mailbox(self.loop)
        address = ActorAddress(mailbox, uuid, self)

        self.store.post(uuid, actor.state)

        future = self.schedule(self.on_stage(actor, address))
        self.performing.append(future)

        return address

    async def on_stage(self, actor, address):
        while True:
            message = await address.mailbox.get()

            state = self.store.get(address.uuid)
            actor.state = state

            #  signal to take the actor out of scene
            if message is None:
                break

            actor.receive(message)


def create_mailbox(loop: AbstractEventLoop):
    return Queue(maxsize=10, loop=loop)
