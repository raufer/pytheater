import asyncio
import threading

from abc import ABC

from types import AsyncGeneratorType
from typing import Coroutine
from typing import Any

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future


class SystemEventLoop(ABC):
    def __init__(self):
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=start_event_loop, args=(self.loop,))
        self.thread.start()

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> Future:
        future = run_coroutine_threadsafe(coro, self.loop)
        return future


def start_event_loop(loop: AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
