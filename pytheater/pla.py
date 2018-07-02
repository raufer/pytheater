import asyncio
import time

from actor import Actor
from actor_system import ActorSystem


class Hello(Actor):

    def receive(self, message):
        time.sleep(2)
        print(f"Received: {message}")

    def __repr__(self):
        return "Actor: Hello"


system = ActorSystem()

actor = system.create_actor(Hello)

print(actor)

actor.tell("Hello World!")
actor.tell("Tell a message")
actor.tell("To the following actor")
