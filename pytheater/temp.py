import asyncio
import random


async def produce(queue):
    item = 'M'
    while True:
        await queue.put(item)
        print(f"Produced {item}")

async def consume(queue):
    while True:
        await asyncio.sleep(2)
        item = await queue.get()
        print(f"Got {item}")

loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop, maxsize=1)
producer_coro = produce(queue)
consumer_coro = consume(queue)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()