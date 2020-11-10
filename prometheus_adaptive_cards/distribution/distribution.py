"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from prometheus_adaptive_cards.config import Target

from .model import Payload


def send(payload: Payload):
    for target in payload.targets:
        url = generate_url(target)
