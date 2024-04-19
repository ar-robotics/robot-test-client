import json


def get_config() -> dict:
    config = {}

    with open("./test_client/config.json", "r") as f:
        config = json.load(f)

    return config
