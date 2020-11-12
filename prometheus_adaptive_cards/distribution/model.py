from pydantic import BaseModel

from prometheus_adaptive_cards.config import Target


class Payload(BaseModel):
    data: dict
    targets: list[Target]
