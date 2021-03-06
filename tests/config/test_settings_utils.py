"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pprint

import pytest
from box import Box

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
        settings_utils.parse_yamls([file1_path.resolve()])


def test_parse_yaml_empty(tmp_path):
    file_content = "---"

    file_path = tmp_path / "file.yml"
    file_path.write_text(file_content)

    contents = settings_utils.parse_yamls([file_path.resolve()])

    assert contents == []


# ==============================================================================
# generate_locations


def test_generate_locations_no_file():
    assert (
        settings_utils.generate_locations(
            [
                "/etc/something/here.yml",
                "sumtim.abc.foo.bar.feec",
                "abc",
            ]
        )
        == []
    )


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
    helpers.print_struct(path_strs, "path_strs")

    path_strs_with_local = settings_utils.generate_locations(path_strs)
    helpers.print_struct(path_strs_with_local, "path_strs_with_local")

    root = tmp_path.resolve()
    assert path_strs_with_local == [
        f"{root}/here.yml",
        f"{root}/here.local.yml",
    ]


# ==============================================================================
# unflatten


def test_unflatten_no_expansion():
    assert settings_utils.unflatten({"a": 12}) == {"a": 12}


def test_unflatten_dotted_path_expansion():
    assert settings_utils.unflatten({"a.b.c": 12}) == {"a": {"b": {"c": 12}}}


def test_unflatten_dotted_path_expansion_multi_overwrite():
    assert settings_utils.unflatten({"a.b.c": 12, "a.b": 10}) == {"a": {"b": 10}}


def test_unflatten_dotted_path_expansion_multi():
    assert settings_utils.unflatten({"a.b.c": 12, "a.d": 10}) == {
        "a": {"b": {"c": 12}, "d": 10}
    }


# ==============================================================================
# cast


def test_cast_non_existing_at_str():
    x = {"foo": {"bar": "hello"}}
    settings_utils.cast(Box(x, box_dots=True), "foo.bar.zoom", str)
    assert True


def test_cast_non_existing_at_int():
    x = {"foo": {"bar": 1}}
    settings_utils.cast(Box(x, box_dots=True), "foo.bar.zoom", str)
    assert True


def test_cast_non_existing_at_boolean():
    x = {"foo": {"bar": True}}
    settings_utils.cast(Box(x, box_dots=True), "foo.bar.zoom", str)
    assert True


def test_cast_to_int_successful():
    x = Box({"foo": {"bar": "32"}}, box_dots=True)
    settings_utils.cast(x, "foo.bar", int)
    assert x.foo.bar == 32


def test_cast_to_float_successful():
    x = Box({"foo": {"bar": "32.12"}}, box_dots=True)
    settings_utils.cast(x, "foo.bar", float)
    assert x.foo.bar == 32.12


def test_cast_to_boolean_successful():
    x = Box({"foo": {"bar": "true"}}, box_dots=True)
    settings_utils.cast(x, "foo.bar", bool)
    assert x.foo.bar is True


def test_cast_to_int_unsuccessful():
    x = Box({"foo": {"bar": "fe"}}, box_dots=True)
    with pytest.raises(ValueError):
        settings_utils.cast(x, "foo.bar", int)


def test_cast_to_bool_unsuccessful():
    x = Box({"foo": {"bar": "fe"}}, box_dots=True)
    settings_utils.cast(x, "foo.bar", bool)
    assert x.foo.bar is False


# ==============================================================================
