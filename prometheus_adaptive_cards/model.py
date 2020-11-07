"""
This module contains the model that is handed over to the templating engine.
Notice that the API itself does not use this model. Initially the data is
processed as a nested dictionary.

Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0
"""

from dataclasses import dataclass
from datetime import datetime

from fastapi import Request


@dataclass
class Alert:
    fingerprint: str
    status: str
    starts_at: datetime
    ends_at: datetime
    generator_url: str
    labels: dict[str, str]
    annotations: dict[str, str]
    specific_annotations: dict[str, str]
    specific_labels: dict[str, str]

    def __post_init__(self):
        if not isinstance(self.starts_at, str):
            self.starts_at = datetime.strptime(self.starts_at[:19], r"%Y-%m-%dT%H:%M:%S")
        if not isinstance(self.ends_at, str):
            self.ends_at = datetime.strptime(self.ends_at[:19], r"%Y-%m-%dT%H:%M:%S")


@dataclass
class AlertGroup:
    receiver: str
    status: str
    external_url: str
    version: str
    group_key: str
    truncated_alerts: int
    group_labels: dict[str, str]
    common_labels: dict[str, str]
    common_annotations: dict[str, str]
    request: Request
    alerts: list[Alert]
