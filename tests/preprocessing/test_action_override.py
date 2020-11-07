"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import re

import pytest

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Override, Route, Routing

# ==============================================================================


@pytest.mark.actions_override
def test_override():
    target = "labels"
    items = {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    data = {
        f"common_{target}": {
            "tim": "schwenke",
        },
        "alerts": [
            {
                target: {
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            },
            {
                target: {
                    "tim": "schwenke",
                }
            },
        ],
    }

    actions._override(target, items, data)
    assert data == {
        f"common_{target}": {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        "alerts": [
            {
                target: {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
            {
                target: {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


# ==============================================================================


@pytest.mark.actions_wrapped_override
def test_wrapped_override_none_none():
    data = {
        f"common_labels": {
            "tim": "schwenke",
            "hans": "meier",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            },
            {
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            },
        ],
    }
    o1 = None
    o2 = None
    actions.wrapped_override(o1, o2, data)
    assert data == {
        f"common_labels": {
            "tim": "schwenke",
            "hans": "meier",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            },
            {
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            },
        ],
    }


@pytest.mark.actions_wrapped_override
def test_wrapped_override_o1_none():
    data = {
        f"common_labels": {
            "tim": "schwenke",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwenke",
                }
            },
        ],
    }
    o1 = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    o2 = None
    actions.wrapped_override(o1, o2, data)
    assert data == {
        "common_labels": {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


@pytest.mark.actions_wrapped_override
def test_wrapped_override_none_o2():
    data = {
        f"common_labels": {
            "tim": "schwenke",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwenke",
                }
            },
        ],
    }
    o2 = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    o1 = None
    actions.wrapped_override(o1, o2, data)
    assert data == {
        "common_labels": {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


@pytest.mark.actions_wrapped_override
def test_wrapped_override_o1_o2():
    data = {
        f"common_labels": {
            "tim": "schwenke",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwenke",
                }
            },
        ],
    }
    o1 = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
        }
    )
    o2 = Override(
        labels={
            "ute": "freier",
            "frank": "sohn",
        }
    )
    actions.wrapped_override(o1, o2, data)
    assert data == {
        "common_labels": {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        "alerts": [
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
            {
                "labels": {
                    "tim": "schwonkel",
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


# ==============================================================================
