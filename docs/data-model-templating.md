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

The following schema uses (pseudo) Python just because it's really readable.

```python
Data:
    receiver: str
    status: str
    external_url: str
    version: str
    group_key: str
    truncated_alerts: int = 0
    group_labels: dict[str, str]
    common_labels: dict[str, str]
    common_annotations: dict[str, str]
    alerts: list[Alert]

    # FastAPI request object.
    request: Request
```

```python
Alert:
    fingerprint: str
    status: str
    starts_at: datetime
    ends_at: datetime
    generator_url: str
    labels: dict[str, str]
    annotations: dict[str, str]

    # Annotations that are not common annotations.
    specific_labels: dict[str, str]

    # Labels that are not common labels.
    specific_annotations: dict[str, str]
```

## Technical Info

The API model is located at `prometheus_adaptive_cards/api/models.py` and uses
Pydantic. 

After receiving it, it goes through a number of preprocessing steps
(removing, adding, overriding) and the additional fields you can see in
["Schema"](#schema) are added **not** directly to the model in
`prometheus_adaptive_cards/preprocessing/enhancement.py`. 

It is in fact first turned into a dict, then the fields are added, then a new
enhanced model is constructed from this dict. This is due to the way Pydantic
works. The enhanced model is located in `prometheus_adaptive_cards/preprocessing/enhancement.py`.
