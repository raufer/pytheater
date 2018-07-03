import asyncio
import threading

from abc import ABC

from types import AsyncGeneratorType

from asyncio import AbstractEventLoop
from asyncio import run_coroutine_threadsafe
from asyncio import Future

from utils.async import start_event_loop


class SystemThread(ABC):
    def __init__(self):
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=start_event_loop, args=(self.loop,))
        self.thread.start()

    def schedule(self, coro: AsyncGeneratorType) -> Future:
        future = run_coroutine_threadsafe(coro, self.loop)
        return future



