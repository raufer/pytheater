import asyncio
import threading

from typing import Coroutine

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future
from asyncio.queues import Queue

from pytheater.actor_address import ActorAddress
from pytheater.store import Store
from pytheater.utils import gen_uuid


class ActorSystem:

    def __init__(self):
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        self.actors_in_play = []

        self.thread = threading.Thread(target=start_event_loop, args=(self.loop,))
        self.thread.start()

    def create_actor(self, actor_class) -> ActorAddress:
        actor = actor_class(system=self)
        mailbox = create_mailbox(self.loop)
        address = ActorAddress(destination=mailbox, uuid=gen_uuid(), system=self)

        self.actors_in_play.append(self.schedule(self.on_stage(actor, mailbox)))
        return address

    def schedule(self, coro: Coroutine) -> Future:
        future = run_coroutine_threadsafe(coro, self.loop)
        return future

    async def on_stage(self, actor, mailbox):
        while True:
            message = await mailbox.get()

            #  signal to take the actor out of scene
            if message is None:
                break

            actor.receive(message)


def start_event_loop(loop:AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def create_mailbox(loop: AbstractEventLoop):
    return Queue(maxsize=10, loop=loop)
