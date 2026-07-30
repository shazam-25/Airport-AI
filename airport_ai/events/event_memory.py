import time
from airport_ai.config import config


class EventMemory:
    def __init__(self, cooldown_seconds):
        self.memory={}
        self.cooldown = cooldown_seconds

    def allow(self,key):
        now=time.time()
        last_seen = self.memory.get(key)
        if last_seen is None:
            self.memory[key] = now
            return True

        if now - last_seen > self.cooldown:
            self.memory[key] = now
            return True

        return False