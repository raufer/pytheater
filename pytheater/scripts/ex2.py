import asyncio
import time

from pytheater.actor import Actor
from pytheater.core.actor_system import ActorSystem

N = 100


class PiMaster(Actor):
    async def receive(self, message, sender):
        if message == 'Calculate PI':
            print("Master: Calculating PI")
            result = await self.calculate_pi()
            print("on receive", result)
            sender.tell(result)

    async def calculate_pi(self):
        workers = [self.system.create_actor(PiWorker) for _ in range(10)]

        for i, actor in enumerate(workers):
            actor.tell({
                'action': 'Calculate PI Part',
                'from': i * 10,
                'to': (i + 1) * 10
            })


class PiWorker(Actor):

    async def receive(self, message, sender):
        if message['action'] == 'Calculate PI Part':
            partial = [(-1) ** n / (2 * n + 1) for n in range(message['from'], message['to'])]
            sender.tell(partial)


system = ActorSystem()

actor = system.create_actor(PiMaster)

result = actor.ask('Calculate PI')
print("FUTURE", result)
print("RESULT", result.result())
print("RESULT**2", result.result().result())
