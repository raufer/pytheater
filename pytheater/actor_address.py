from asyncio import Future


class ActorAddress:

    def __init__(self, mailbox, uuid, system):
        self.mailbox = mailbox
        self.uuid = uuid
        self.system = system

    def tell(self, message):
        self.system.tell(self.mailbox, message)

    def ask(self, message) -> Future:
        return self.system.ask(self.mailbox, message).result()

    def __repr__(self):
        return f"Address: [{self.uuid}]"
