import asyncio

from threading import Thread

asyncio.Future

loop = asyncio.new_event_loop()


def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


t = Thread(target=run_event_loop, args=(loop,))
t.start()

async def f(x):
    res = await g(x / 2)
    return res

async def g(x):
    return x * 2


x = 10

future = asyncio.run_coroutine_threadsafe(f(x), loop)

print(future)  # <Future at 0x106f797f0 state=pending>
print(future.result())  # <Future at 0x10677c780 state=finished returned float>
print(future.result().result())  # 10.0
print(type(future))




