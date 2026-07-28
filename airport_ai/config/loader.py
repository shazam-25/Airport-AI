import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, path):
        self.path = Path(path)
        self.config = self.load()
    
    def load(self):
        with open(self.path, "r") as file:
            return yaml.safe_load(file)

    def get(self, key):
        return self.config.get(key)