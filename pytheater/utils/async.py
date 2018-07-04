import asyncio

from asyncio import AbstractEventLoop
from asyncio.queues import Queue


async def await_put(queue: Queue, item):
    await queue.put(item)


async def await_get(queue: Queue):
    item = await queue.get()
    return item
