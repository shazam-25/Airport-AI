from airport_ai.config.loader import ConfigLoader
from airport_ai.config.schemas import validate

config = ConfigLoader("Airport-AI/airport_ai/config/loader.py")

validate(config.config)