"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import re

import pytest

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Add, Route, Routing

# ==============================================================================


@pytest.mark.actions_add
def test_add():
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

    actions._add(target, items, data)
    assert data == {
        f"common_{target}": {
            "tim": "schwenke",
            "frank": "sohn",
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
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


# ==============================================================================


@pytest.mark.actions_wrapped_add
def test_wrapped_add_none_none():
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
    a1 = None
    a2 = None
    actions.wrapped_add(a1, a2, data)
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


@pytest.mark.actions_wrapped_add
def test_wrapped_add_a1_none():
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
    a1 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    a2 = None
    actions.wrapped_add(a1, a2, data)
    assert data == {
        "common_labels": {
            "tim": "schwenke",
            "frank": "sohn",
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
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


@pytest.mark.actions_wrapped_add
def test_wrapped_add_none_a2():
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
    a2 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    a1 = None
    actions.wrapped_add(a1, a2, data)
    assert data == {
        "common_labels": {
            "tim": "schwenke",
            "frank": "sohn",
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
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


@pytest.mark.actions_wrapped_add
def test_wrapped_add_a1_a2():
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
    a1 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
        }
    )
    a2 = Add(
        labels={
            "ute": "freier",
            "frank": "sohn",
        }
    )
    actions.wrapped_add(a1, a2, data)
    assert data == {
        "common_labels": {
            "tim": "schwenke",
            "frank": "sohn",
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
                    "ute": "freier",
                    "frank": "sohn",
                }
            },
        ],
    }


# ==============================================================================
