from pytheater.actor import Actor


class AnonymousActor(Actor):
    def receive(self, message, sender=None):
        return message
