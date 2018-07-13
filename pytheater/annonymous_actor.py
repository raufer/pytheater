from pytheater.actor import Actor


class AnonymousActor(Actor):
    async def receive(self, message, sender=None):
        return message
