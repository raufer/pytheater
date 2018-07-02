import asyncio
import threading

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future


class ActorSystem:

    def __init__(self):
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        self.registry = []

        self.thread = threading.Thread(target=start_event_loop, args=(self.loop,))
        self.thread.start()

    def create_actor(self, actor_class) -> 'Actor':
        actor = actor_class(system=self)
        run_coroutine_threadsafe(actor.run(), self.loop)
        self._register(actor)
        return actor

    def schedule(self, coro) -> Future:
        future = run_coroutine_threadsafe(coro, self.loop)
        return future

    def _register(self, actor):
        self.registry.append(actor)


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()