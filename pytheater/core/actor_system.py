import asyncio
import threading
import logging

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future
from asyncio.queues import Queue

from pytheater.annonymous_actor import AnonymousActor
from pytheater.core import SystemEventLoop
from pytheater.actor_address import ActorAddress
from pytheater.core.store import Store
from pytheater.utils.identifier import gen_uuid


logger = logging.getLogger(__name__)


class ActorSystem(SystemEventLoop):
    def __init__(self):
        self.performing = []
        self.store = Store()
        super(ActorSystem, self).__init__()

    def create_actor(self, actor_class, **kwargs) -> ActorAddress:
        actor, address = self.spawn(actor_class, **kwargs)
        self.store.post(address.uuid, actor.state)

        future = self.schedule(self.run_forever(actor, address))
        self.performing.append(future)

        logger.info(f"Created an actor of class '{actor_class.__name__}' ({kwargs})")
        return address

    def spawn(self, actor_class, **kwargs):
        uuid = gen_uuid()
        actor = actor_class(system=self, uuid=uuid)
        actor.constructor(**kwargs)

        mailbox = create_mailbox(self.loop)
        address = ActorAddress(mailbox, uuid, self)

        return actor, address

    async def run_forever(self, actor, address):
        while True:
            try:
                message, sender = await address.mailbox.get()

                state = self.store.get(address.uuid)
                actor.state = state

                #  signal to take the actor out of scene
                if message is None:
                    break

                await actor.receive(message, sender)
            except Exception as e:
                print(e)

    async def run_once(self, actor, address):
        try:
            message, sender = await address.mailbox.get()
            response = await actor.receive(message, sender)
            return response
        except Exception as e:
            print("exiting via exception")
            print(e)

    def invited_guest(self):
        guest_actor, guest_address = self.spawn(AnonymousActor)
        future = self.schedule(self.run_once(guest_actor, guest_address))
        return future, guest_address


def create_mailbox(loop: AbstractEventLoop):
    return Queue(maxsize=10, loop=loop)
