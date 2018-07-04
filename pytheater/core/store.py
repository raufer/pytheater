import asyncio

from asyncio.queues import Queue

from pytheater.core import SystemEventLoop
from pytheater.utils.async import await_put, await_get


class Store(SystemEventLoop):
    def __init__(self):
        self.channels = {}
        super(Store, self).__init__()

    def get(self, uuid):
        queue = self.channels[uuid]
        future = self.schedule(await_get(queue))
        return future.result()

    def post(self, uuid, state):
        queue = Queue(maxsize=1)
        self.channels[uuid] = queue
        future = self.schedule(await_put(queue, state))
        return future.result()

    def put(self, uuid, current_state, next_state):
        queue = self.channels[uuid]

        self.schedule(self.state_update(queue, current_state, next_state))

    def delete(self, uuid):
        self.channels.pop(uuid)

    async def state_update(self, queue, current_state, next_state):
        new_state = {
            **current_state,
            **next_state
        }

        await queue.put(new_state)
