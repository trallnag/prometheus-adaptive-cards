"""
Shall contain code that enhances the data as part of the preprocessing step
before handing it over to the actual templating code. It works by introducing
an internal (enhanced) model of the API model.

    ? I feel like the way the enhancement is applied is ugly. But I can't think
    ? of a better way to do it with Pydantic. I guess I could convert the whole
    ? tree into a Box and be done with Pydantic but I'd rather not.

Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0
"""


from fastapi import Request
from pydantic import Field

from prometheus_adaptive_cards.api.models import Alert, Data

# ==============================================================================


class EnhancedAlert(Alert):
    """Enhances Alert object with additional information."""

    specific_annotations: dict[str, str] = Field(
        title="Specific Annotations",
        description="Annotations that are NOT common annotations.",
    )
    specific_labels: dict[str, str] = Field(
        title="Specific Annotations", description="Labels that are NOT common labels."
    )


class EnhancedData(Data):
    """Enhances Data object with additional information."""

    request: str = Field(
        title="Request", description="Request object (that also contains raw payload)."
    )
    alerts: list[EnhancedAlert] = Field(title="Alerts")

    class Config:
        arbitrary_types_allowed = True


# ==============================================================================


def enhance_data(request: Request, data: Data) -> EnhancedData:
    """Enhances data in-place by adding attributes.

    Technical info: What this function does is really simple, but it is done in
    a quite convuluted way due to features / limits in Pydantic. It is not
    possible to add attributes to a Pydantic model instance. Therefore another
    set of models has been created. So the base models are turned into dicts,
    mutated and then converted into the new models. This has to be done in
    layers because `construct` does not work with nested models.

        ? Might require refactoring in the future in case I want to add a bunch
        ? more enhancements. But for now it works fine.

    Args:
        request (Request): Request object
        data (Data): Data where attributes will be added to.
    """

    data = data.dict()

    data["request"] = request

    enhanced_alerts = []

    for alert in data["alerts"]:
        enhanced_alerts.append(
            EnhancedAlert.construct(
                **alert,
                specific_annotations={
                    k: alert["annotations"][k]
                    for k in set(alert["annotations"]) - set(data["common_annotations"])
                },
                specific_labels={
                    k: alert["labels"][k]
                    for k in set(alert["labels"]) - set(data["common_labels"])
                }
            )
        )

    data["alerts"] = enhanced_alerts

    data = EnhancedData.construct(**data)
    return data


# ==============================================================================
