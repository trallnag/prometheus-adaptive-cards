from pydantic import BaseModel, Json

from prometheus_adaptive_cards.config import Target


class Payload(BaseModel):
    data: Json
    targets: list[Target]