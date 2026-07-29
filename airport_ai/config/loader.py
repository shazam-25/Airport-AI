import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, path):
        self.path = Path(path).resolve()
        print(f"Loading configuration: {self.path}")
        self.project_root = self.path.parents[2]
        print("Project root:", self.project_root)
        self.config = self.load()
    
    def load(self):
        with open(self.path, "r") as file:
            return yaml.safe_load(file)

    def get(self, key):
        return self.config.get(key)
    
    def resolve_path(self, value):
        path = Path(value)
        if path.is_absolute():
            return str(path)
        return str(self.project_root / path)