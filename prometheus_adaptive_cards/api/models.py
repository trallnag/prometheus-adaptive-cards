"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0

Defines with the help of pydantic models the payload send in from Prometheus
Alertmanager. The payload is not changed / enhanced whatsoever in this module.
Follows more or less the official model defined [here](https://github.com/prometheus/alertmanager/blob/master/template/template.go
and [here](https://prometheus.io/docs/alerting/latest/notifications/).
"""

from datetime import datetime

from pydantic import AnyUrl, BaseModel, Field


class Alert(BaseModel):
    """https://github.com/prometheus/alertmanager/blob/master/docs/notifications.md#alert"""

    fingerprint: str = Field(title="Fingerprint")
    status: str = Field(title="Status")
    starts_at: datetime = Field(title="Starts At", alias="startsAt")
    ends_at: datetime = Field(title="Ends At", alias="endsAt")
    generator_url: AnyUrl = Field(title="Generator URL", alias="generatorURL")
    labels: dict[str, str] = Field(title="Labels")
    annotations: dict[str, str] = Field(title="Annotations")

    class Config:
        schema_extra = {
            "example": {
                "fingerprint": "ff6a7a0f5f1c1309",
                "status": "firing",
                "startsAt": "2020-10-11T14:34:11.279383004Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "https://domain.com/promstack/prometheus/graph?g0.expr=max+by%28namespace%2C+name%29+%28%28avg_over_time%28container_memory_working_set_bytes%5B5m%5D%29+%3E+avg_over_time%28container_memory_rss%5B5m%5D%29+or+avg_over_time%28container_memory_rss%5B5m%5D%29%29+%2F+on%28namespace%2C+name%2C+id%29+avg_over_time%28container_spec_memory_reservation_limit_bytes%5B5m%5D%29+%21%3D+%2BInf%29+%2A+100+%3C+40&g0.tab=1",
                "labels": {
                    "alertname": "JustATestAlert",
                    "name": "grafana",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                },
                "annotations": {
                    "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr some unique value 1.",
                    "investigate_link": "https://domain.com/grafana/d/fdwTIxFMz/container-intra",
                    "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                    "startsAt": "2020-10-11T14:34:11.279383004Z",
                },
            }
        }


class Data(BaseModel):
    """https://github.com/prometheus/alertmanager/blob/master/docs/notifications.md#data"""

    receiver: str = Field(title="Receiver")
    status: str = Field(title="Status")
    external_url: AnyUrl = Field(title="External URL", alias="externalURL")
    version: str = Field(title="Version")
    group_key: str = Field(title="Group Key", alias="groupKey")
    group_labels: dict[str, str] = Field(title="Group Labels", alias="groupLabels")
    common_labels: dict[str, str] = Field(title="Common Labels", alias="commonLabels")
    common_annotations: dict[str, str] = Field(
        title="Common Annotations", alias="commonAnnotations"
    )
    alerts: list[Alert] = Field(title="Alerts")

    class Config:
        schema_extra = {
            "example": {
                "receiver": "cisco webex",
                "status": "firing",
                "externalURL": "https://domain.com/promstack/alertmanager",
                "version": "4",
                "groupKey": '{}/{namespace="whatever/promstack"}:{alertname="JustATestAlert"}',
                "groupLabels": {
                    "alertname": "JustATestAlert",
                    "namespace": "whatever/promstack",
                },
                "commonLabels": {
                    "alertname": "JustATestAlert",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                },
                "commonAnnotations": {
                    "investigate_link": "https://domain.com/grafana/d/fdwTIxFMz/container-intra",
                    "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                },
                "alerts": [
                    {
                        "fingerprint": "ff6a7a0f5f1c1309",
                        "status": "firing",
                        "startsAt": "2020-10-11T14:34:11.279383004Z",
                        "endsAt": "0001-01-01T00:00:00Z",
                        "generatorURL": "https://domain.com/promstack/prometheus/graph?g0.expr=max+by%28namespace%2C+name%29+%28%28avg_over_time%28container_memory_working_set_bytes%5B5m%5D%29+%3E+avg_over_time%28container_memory_rss%5B5m%5D%29+or+avg_over_time%28container_memory_rss%5B5m%5D%29%29+%2F+on%28namespace%2C+name%2C+id%29+avg_over_time%28container_spec_memory_reservation_limit_bytes%5B5m%5D%29+%21%3D+%2BInf%29+%2A+100+%3C+40&g0.tab=1",
                        "labels": {
                            "alertname": "JustATestAlert",
                            "name": "grafana",
                            "namespace": "whatever/promstack",
                            "severity": "info",
                        },
                        "annotations": {
                            "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr some unique value 1.",
                            "investigate_link": "https://domain.com/grafana/d/fdwTIxFMz/container-intra",
                            "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
                            "title": "Memory: Relativ memory usage low",
                            "startsAt": "2020-10-11T14:34:11.279383004Z",
                        },
                    },
                    {
                        "fingerprint": "ff6a7a0f5f1c1409",
                        "status": "firing",
                        "startsAt": "2020-10-11T14:34:11.279383004Z",
                        "endsAt": "0001-01-01T00:00:00Z",
                        "generatorURL": "https://domain.com/promstack/prometheus/graph?g0.expr=max+by%28namespace%2C+name%29+%28%28avg_over_time%28container_memory_working_set_bytes%5B5m%5D%29+%3E+avg_over_time%28container_memory_rss%5B5m%5D%29+or+avg_over_time%28container_memory_rss%5B5m%5D%29%29+%2F+on%28namespace%2C+name%2C+id%29+avg_over_time%28container_spec_memory_reservation_limit_bytes%5B5m%5D%29+%21%3D+%2BInf%29+%2A+100+%3C+40&g0.tab=1",
                        "labels": {
                            "alertname": "JustATestAlert",
                            "name": "grafana",
                            "namespace": "whatever/promstack",
                            "severity": "info",
                        },
                        "annotations": {
                            "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr some unique value 2.",
                            "investigate_link": "https://domain.com/grafana/d/fdwTIxFMz/container-intra",
                            "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
                            "title": "Memory: Relativ memory usage low",
                            "startsAt": "2020-10-11T14:34:11.279393004Z",
                        },
                    },
                ],
            }
        }
