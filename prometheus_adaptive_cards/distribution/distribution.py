from .model import Payload


def send(payload: Payload):
    for target in payload.targets:
        url = generate_url(target)
