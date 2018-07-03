import asyncio

from asyncio import AbstractEventLoop
from asyncio.queues import Queue


def start_event_loop(loop: AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def await_put(queue: Queue, item):
    await queue.put(item)


async def await_get(queue: Queue):
    item = await queue.get()
    return item
