"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pprint
import textwrap

import pytest

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
# parse_yamls


def test_parse_yaml(tmp_path):
    file1_content = """\
    hallo:
      welt: wie geht es dir
      name: tim schwenke
      some_list:
        - fefewfw
        - 322
    """
    file1_path = tmp_path / "file1.yml"
    file1_path.write_text(file1_content)
    assert file1_path.read_text() == file1_content

    file2_content = """\
    hallo:
      welt: wie geht es dir
      name: thomas
      some_list:
        - fefewfw
        - 322
        - 34
    """
    file2_path = tmp_path / "file2.yml"
    file2_path.write_text(file2_content)
    assert file2_path.read_text() == file2_content

    file3_content = """\
    hallo:
      foo: bar
    """
    file3_path = tmp_path / "file3.yml"
    file3_path.write_text(file3_content)
    assert file2_path.read_text() == file2_content

    contents = settings_utils.parse_yamls(
        [
            file1_path.resolve(),
            file2_path.resolve(),
            file3_path.resolve(),
            tmp_path.resolve(),
        ]
    )

    assert contents[0] == {
        "hallo": {
            "welt": "wie geht es dir",
            "name": "tim schwenke",
            "some_list": ["fefewfw", 322],
        }
    }

    assert contents[1] == {
        "hallo": {
            "welt": "wie geht es dir",
            "name": "thomas",
            "some_list": ["fefewfw", 322, 34],
        }
    }

    assert contents[2] == {"hallo": {"foo": "bar"}}


def test_parse_invalid(tmp_path):
    file1_content = """\
    - wier
    tom = 22
    """
    file1_path = tmp_path / "file1.yml"
    file1_path.write_text(file1_content)
    assert file1_path.read_text() == file1_content

    with pytest.raises(Exception):
        parsed_content = settings_utils.parse_yamls([file1_path.resolve()])


# ==============================================================================
# generate_locations


def test_generate_locations_no_file():
    assert settings_utils.generate_locations(
        [
            "/etc/something/here.yml",
            "sumtim.abc.foo.bar.feec",
            "abc",
        ]
    ) == []


def test_generate_locations_valid(helpers, tmp_path):
    f1 = tmp_path / "here.yml"
    f1.write_text(".")
    (tmp_path / "here.local.yml").write_text(".")
    
    f2 = tmp_path / "sumtim.abc.foo.bar.feec"
    f2.write_text(".")
    (tmp_path / "sumtim.abc.foo.bar.local.feec").write_text(".")
    f3 = tmp_path / "abc"
    f3.write_text(".")

    path_strs = [str(f1.resolve()), str(f2.resolve()), str(f3.resolve())]
    helpers.pp(path_strs, "path_strs")

    path_strs_with_local = settings_utils.generate_locations(path_strs)
    helpers.pp(path_strs_with_local, "path_strs_with_local")

    root = tmp_path.resolve()
    assert path_strs_with_local == [
        f"{root}/here.yml",
        f"{root}/here.local.yml",
    ]


# ==============================================================================
