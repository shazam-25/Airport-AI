REQUIRED_KEYS = [
    "cameras",
    "model",
    "tracking",
    "turnaround",
    "ppe",
    "fod",
    "database"
]

def validate(config):
    for key in REQUIRED_KEYS:
        if key not in config:
            raise Exception(f"Missing config: {key}")