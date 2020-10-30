"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pytest
import pprint
import prometheus_adaptive_cards.config.settings_utils as settings_utils


# ==============================================================================
# merge


def test_merge_dict_with_list():
    target = {
        "foo": "bar",
        "zoom": ["fruktose", "apple"],
        "room": [
            {"dancer": "belly"},
            {"table": "pole"},
            "ting",
        ],
    }

    source = {
        "foo": "zoom",
        "zoom": ["fruktose"],
        "room": [
            {"dancer": "fooba"},
            {"table": "pole"},
            "something",
        ],
    }

    settings_utils.merge(target=target, source=source)
    pprint.pprint(target)

    assert target["foo"] == "zoom"
    assert target["zoom"] == ["fruktose", "apple", "fruktose"]
    assert target["room"] == [
        {"dancer": "belly"},
        {"table": "pole"},
        "ting",
        {"dancer": "fooba"},
        {"table": "pole"},
        "something",
    ]


def test_merge_with_nested_dict():
    target = {"level1": {"level2a": "value", "level2b": {"hallo": "world"}}}
    source = {"level1": {"level2a": "value", "level2b": {"hallo": "test"}}}

    settings_utils.merge(target=target, source=source)
    pprint.pprint(target)

    assert target["level1"]["level2b"]["hallo"] == "test"


def test_merge_with_set():
    target = {"set": set(["a", "b", "c"])}
    source = {"set": set(["a", "d"])}

    settings_utils.merge(target=target, source=source)
    pprint.pprint(target)

    assert target["set"] == set(["a", "b", "c", "d"])


def test_merge_multiple():
    target = {"a": "1"}
    source = [
        {"a": "2"},
        {"a": "3"},
    ]

    settings_utils.merge(target=target, source=source)
    pprint.pprint(target)

    assert target["a"] == "3"


def test_merge_multiple():
    target = {"a": "1"}
    source = [
        {"a": "2"},
        {"a": "3"},
    ]

    settings_utils.merge(target=target, source=source)
    pprint.pprint(target)

    assert target["a"] == "3"


# ==============================================================================
