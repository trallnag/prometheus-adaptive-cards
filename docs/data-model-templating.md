# Data Model for Usage in Templating

This document refers to the model that is used from within templating code,
not the data model for the API which exactly matches the official Alertmanager
model you for example find [here](https://github.com/prometheus/alertmanager/blob/master/docs/notifications.md#data).

From all templating options (may it be a Jinja template or pure Python script),
this data model is available under the `data` keyword. It contains the vanilla
model with a few additional fields. Also a few names differ to comply with
the way fields should be named in Python (for example `starts_at` instead of
`startsAt`).

## Schema

The module containing the following classes can be found at `prometheus_adaptive_cards/model.py`.

```python
@dataclass
class EnhancedAlert:
    fingerprint: str
    status: str
    starts_at: datetime
    ends_at: datetime
    generator_url: str
    labels: dict[str, str]
    annotations: dict[str, str]
    specific_annotations: dict[str, str]
    specific_labels: dict[str, str]


@dataclass
class EnhancedData:
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
    alerts: list[EnhancedAlert]
```

## Technical Info

The model can be separated into an external and internal view. The external view
uses Pydantic and validated the payload that is handed over to a route endpoint.
Then the data goes through a preprocessing pipeline as a raw dictionary. At the
end of the pipeline the data is injected into a set of dataclass objects that
are handed over to the templating engine.

You can find both the internal and external model at `prometheus_adaptive_cards/model.py`.
