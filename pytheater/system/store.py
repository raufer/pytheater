import asyncio
import threading

from asyncio import AbstractEventLoop
from asyncio.queues import Queue

from system import SystemThread
from utils.async import start_event_loop, await_put


class Store(SystemThread):
    def __init__(self):
        self.data = {}
        super(Store, self).__init__()

    def register_new_state(self, uuid, state):
        queue = Queue(maxsize=1)
        queue.put_nowait(state)
        self.data[uuid] = queue

    def update_state(self, uuid, next_state):
        current_state = self.data[uuid]

        new_state = {
            **current_state,
            **next_state
        }

        self.schedule(await_put(queue=self.data[uuid], item=new_state))

    async def await_put(self, uuid, next_state):
        current_state = self.data[uuid].get()

        new_state = {
            **current_state,
            **next_state
        }

        await queue.put(item)
