import logging

from asyncio import Future

from typing import Any


class ActorAddress:

    def __init__(self, mailbox, uuid, system):
        self.mailbox = mailbox
        self.uuid = uuid
        self.system = system

    def tell(self, message):
        self.system.schedule(self._tell(message))

    async def _tell(self, message: Any):
        await self.mailbox.put((message, None))

    def ask(self, message) -> Future:
        return self.system.schedule(self._ask(message))

    async def _ask(self, message: Any):
        future_answer, guest_address = self.system.invited_guest()
        await self.mailbox.put((message, guest_address))
        return future_answer

    def __repr__(self):
        return f"Address: [{self.uuid}]"
