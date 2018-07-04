

class ActorAddress:

    def __init__(self, mailbox, uuid, system):
        self.mailbox = mailbox
        self.uuid = uuid
        self.system = system

    async def send(self, message):
        await self.mailbox.put(message)

    def tell(self, message):
        print(f"Telling message {message}")
        self.system.schedule(self.send(message))

    def __repr__(self):
        return f"Address: [{self.uuid}]"
