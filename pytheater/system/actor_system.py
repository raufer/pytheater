import asyncio
import threading

from typing import Coroutine

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future
from asyncio.queues import Queue

from system import SystemThread
from utils.async import start_event_loop
from pytheater.actor_address import ActorAddress
from pytheater.store import Store
from pytheater.utils.identifier import gen_uuid


class ActorSystem(SystemThread):

    def __init__(self):
        self.actors_in_play = []
        super(ActorSystem, self).__init__()

    def create_actor(self, actor_class) -> ActorAddress:
        actor = actor_class(system=self)
        mailbox = create_mailbox(self.loop)
        address = ActorAddress(destination=mailbox, uuid=gen_uuid(), system=self)
        self.actors_in_play.append(self.schedule(self.on_stage(actor, mailbox)))
        return address

    async def on_stage(self, actor, mailbox):
        while True:
            message = await mailbox.get()

            #  signal to take the actor out of scene
            if message is None:
                break

            actor.receive(message)


def create_mailbox(loop: AbstractEventLoop):
    return Queue(maxsize=10, loop=loop)
