"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from datetime import datetime

from pydantic import BaseModel, Field

from prometheus_adaptive_cards.config import Target

# ==============================================================================


class Alert(BaseModel):
    fingerprint: str
    status: str
    starts_at: datetime = Field(alias="startsAt")
    ends_at: datetime = Field(alias="endsAt")
    generator_url: str = Field(alias="generatorURL")
    labels: dict[str, str]
    annotations: dict[str, str]

    class Config:
        extra = "allow"


class AlertGroup(BaseModel):
    receiver: str
    status: str
    external_url: str = Field(alias="externalURL")
    version: str
    group_key: str = Field(alias="groupKey")
    truncated_alerts: int = Field(alias="truncatedAlerts", default=0)
    group_labels: dict[str, str] = Field(alias="groupLabels")
    common_labels: dict[str, str] = Field(alias="commonLabels")
    common_annotations: dict[str, str] = Field(alias="commonAnnotations")
    alerts: list[Alert]

    class Config:
        extra = "allow"


# ==============================================================================


class EnhancedAlert(Alert):
    specific_annotations: dict[str, str]
    specific_labels: dict[str, str]


class EnhancedAlertGroup(AlertGroup):
    targets: list[Target]


# ==============================================================================
