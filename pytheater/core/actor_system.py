import asyncio
import threading

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future
from asyncio.queues import Queue

from pytheater.annonymous_actor import AnonymousActor
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
        actor, address = self.spawn(actor_class)

        self.store.post(address.uuid, actor.state)

        future = self.schedule(self.enter_in_stage(actor, address))
        self.performing.append(future)

        return address

    def spawn(self, actor_class):
        uuid = gen_uuid()
        actor = actor_class(system=self, uuid=uuid)
        actor.constructor()

        mailbox = create_mailbox(self.loop)
        address = ActorAddress(mailbox, uuid, self)

        return actor, address

    async def enter_in_stage(self, actor, address):
        while True:
            message, sender = await address.mailbox.get()

            state = self.store.get(address.uuid)
            actor.state = state

            #  signal to take the actor out of scene
            if message is None:
                break

            actor.receive(message, sender)

    def tell(self, mailbox, message):
        self.schedule(self._tell(mailbox, message))

    async def _tell(self, mailbox, message):
        await mailbox.put((message, None))

    def ask(self, mailbox, message):
        return self.schedule(self._ask(mailbox, message))

    async def _ask(self, mailbox, message):
        guest_actor, guest_address = self.spawn(AnonymousActor)

        future = self.schedule(self.invited_guest(guest_actor, guest_address))

        await mailbox.put((message, guest_address))

        return future

    async def invited_guest(self, actor, address):
        message, sender = await address.mailbox.get()
        response = actor.receive(message, sender)
        return response


def create_mailbox(loop: AbstractEventLoop):
    return Queue(maxsize=10, loop=loop)
