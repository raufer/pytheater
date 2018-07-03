

class ActorAddress:

    def __init__(self, destination, uuid, system):
        self.destination = destination
        self.uuid = uuid
        self.system = system

    async def new_message(self, message):
        await self.destination.put(message)

    def tell(self, message):
        print(f"Telling message {message}")
        self.system.schedule(self.new_message(message))

    def __repr__(self):
        return f"Address: [{self.uuid}]"
