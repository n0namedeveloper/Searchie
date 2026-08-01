import asyncio
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        
    async def publish(self, channel: str, message: str):
        for q in self.subscribers[channel]:
            await q.put(message)
            
    def subscribe(self, channel: str) -> asyncio.Queue:
        q = asyncio.Queue()
        self.subscribers[channel].append(q)
        return q
        
    def unsubscribe(self, channel: str, q: asyncio.Queue):
        if q in self.subscribers[channel]:
            self.subscribers[channel].remove(q)

bus = EventBus()
