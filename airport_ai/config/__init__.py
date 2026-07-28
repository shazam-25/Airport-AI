from airport_ai.config.loader import ConfigLoader
from airport_ai.config.schemas import validate
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "config.yaml"
)

config = ConfigLoader(CONFIG_PATH)

validate(config.config)