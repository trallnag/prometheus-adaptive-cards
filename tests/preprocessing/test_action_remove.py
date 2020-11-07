"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import re

import pytest

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Remove, Route, Routing

# ==============================================================================


@pytest.mark.actions_remove
def test_remove():
    target = "labels"
    keys = ["tim", "hans", "ute", "furz", "soda"]
    data = {
        f"common_{target}": {
            "tim": "schwenke",
            "hans": "meier",
        },
        "alerts": [
            {
                target: {
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            },
            {
                target: {
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            },
        ],
    }

    actions._remove(target, keys, data)
    assert data == {
        f"common_{target}": {},
        "alerts": [{target: {"ronald": "fritz"}}, {target: {}}],
    }


# ==============================================================================


@pytest.mark.actions_remove_re
def test_remove_re():
    target = "labels"
    keys = [re.compile("^(tim|hans|ute|furz|soda)$")]
    data = {
        f"common_{target}": {
            "tim": "schwenke",
            "hans": "meier",
        },
        "alerts": [
            {
                target: {
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            },
            {
                target: {
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            },
        ],
    }

    actions._remove_re(target, keys, data)
    assert data == {
        f"common_{target}": {},
        "alerts": [{target: {"ronald": "fritz"}}, {target: {}}],
    }


# ==============================================================================


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_none_none():
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
    r1 = None
    r2 = None
    actions.wrapped_remove(r1, r2, data)
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


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_r1_none():
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
    r1 = Remove(re_labels=[re.compile("^(tim|hans|ute|furz|soda)$")])
    r2 = None
    actions.wrapped_remove(r1, r2, data)
    assert data == {
        f"common_labels": {},
        "alerts": [
            {
                "labels": {
                    "ronald": "fritz",
                }
            },
            {"labels": {}},
        ],
    }


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_none_r2():
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
    r1 = None
    r2 = Remove(re_labels=[re.compile("^(tim|hans|ute|furz|soda)$")])
    actions.wrapped_remove(r1, r2, data)
    assert data == {
        f"common_labels": {},
        "alerts": [
            {
                "labels": {
                    "ronald": "fritz",
                }
            },
            {"labels": {}},
        ],
    }


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_r1_r2():
    data = {
        "common_annotations": {},
        "common_labels": {
            "tim": "schwenke",
            "hans": "meier",
        },
        "alerts": [
            {
                "annotations": {},
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                },
            },
            {
                "annotations": {},
                "labels": {
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                },
            },
        ],
    }
    r1 = Remove(
        labels=["ute", "tim", "furz"],
        annotations=["ute", "tim", "furz"],
    )
    r2 = Remove(
        re_annotations=[re.compile("^(tim|hans)$")],
        re_labels=[re.compile("^(tim|hans)$")],
    )
    actions.wrapped_remove(r1, r2, data)
    assert data == {
        "common_annotations": {},
        "common_labels": {},
        "alerts": [
            {
                "annotations": {},
                "labels": {
                    "ronald": "fritz",
                },
            },
            {"annotations": {}, "labels": {}},
        ],
    }


# ==============================================================================
