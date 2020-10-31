"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pytest
from box import Box

import prometheus_adaptive_cards.config.settings_raw as settings_raw

# ==============================================================================


def test_parse_args():
    args = ["--config_file", "foo/bar.yml"]
    args = settings_raw._parse_args(args)
    assert args["config_file"] == "foo/bar.yml"
    assert args.get("does_not_exist") is None


def test_parse_nothing():
    args = []
    args = settings_raw._parse_args(args)
    assert args.get("does_not_exist") is None


def test_parse_long():
    args = [
        "--logging.level",
        "INFO",
        "-some.ting.else_fefe",
        "324",
    ]
    args = settings_raw._parse_args(args)
    assert args["logging"]["level"] == "INFO"
    assert args["some"]["ting"]["else_fefe"] == "324"


def test_parse_invalid():
    args = ["1"]
    with pytest.raises(ValueError):
        settings_raw._parse_args(args)


# ==============================================================================


def test_parse_files_no_files():
    assert (
        settings_raw._parse_files(force_file="/does_not_exist/", lookup_override=[]) == {}
    )


def test_parse_files_force_file(tmp_path):
    force_file = tmp_path / "force_file.yml"
    force_file.write_text("a: b")

    normal_file = tmp_path / "normal_file.yml"
    normal_file.write_text("a: c")

    dct = settings_raw._parse_files(
        force_file=str(force_file.resolve()), lookup_override=[str(normal_file.resolve())]
    )
    assert dct["a"] == "b"


def test_parse_files_lookup(tmp_path):
    n1 = tmp_path / "n1.yml"
    n1.write_text("a: c")

    n2 = tmp_path / "n2.yml"
    n2.write_text("a: b\nfoo: bar")

    n3 = tmp_path / "n3.yml"
    n3.write_text("a: d")

    files = [
        str(n1.resolve()),
        str(n2.resolve()),
        str(n3.resolve()),
    ]

    dct = settings_raw._parse_files(lookup_override=files)
    assert dct["a"] == "d"
    assert dct["foo"] == "bar"


def test_parse_files_local(tmp_path):
    n1 = tmp_path / "n1.yml"
    n1.write_text("a: c\ntrol: sa")

    (tmp_path / "n1.local.yml").write_text("a: b\nfoo: bar")

    dct = settings_raw._parse_files(lookup_override=[str(n1.resolve())])
    assert dct["a"] == "b"
    assert dct["foo"] == "bar"
    assert dct["trol"] == "sa"


# ==============================================================================


def test_cast_vars(helpers):
    box = Box(
        {
            "logging": {
                "structured": {
                    "custom_serializer": "True",
                    "what": "ever",
                }
            },
            "server": {
                "port": 25,
            },
        },
        box_dots=True,
    )

    settings_raw._cast_vars(box)

    assert isinstance(box.logging.structured.custom_serializer, bool)
    assert box.logging.structured.custom_serializer is True

    assert isinstance(box.server.port, int)
    assert box.server.port == 25

    assert isinstance(box.logging.structured.what, str)
    assert box.logging.structured.what == "ever"


# ==============================================================================


def test_parse_env_vars_empty():
    env_vars = settings_raw._parse_env_vars({})
    assert len(env_vars) == 0


def test_parse_env_vars():
    env_vars = settings_raw._parse_env_vars(
        {
            "PROMAC__LOGGING__LEVEL": "what",
            "PROMAC__FOO_BAR": "3",
            "NOTHING": "fe",
        }
    )
    print(env_vars)
    assert len(env_vars) == 2
    assert env_vars["logging.level"] == "what"
    assert env_vars.logging.level == "what"
    assert env_vars["foo_bar"] == "3"
    # Opened an issue to support this [here](https://github.com/cdgriffith/Box/issues/176)
    assert env_vars.get("logging.level") is None


# ==============================================================================


def test_setup_raw_settings(tmp_path, helpers):
    file_content = """\
    logging:
      level: INFO
      format: whatever
      unstructured:
        fmt: lol
    server:
      host: hallo
    and_so_on: huy
    """
    file_path = tmp_path / "file.yml"
    file_path.write_text(file_content)
    assert file_path.read_text() == file_content

    x = settings_raw.setup_raw_settings(
        cli_args=[
            "--config_file",
            str(file_path.resolve()),
            "--logging.structured.custom_serializer",
            "True",
            "--what.ever",
            "hallo",
            "--logging.level",
            "ERROR",
        ],
        env={
            "WHATEVER": "feiohfio",
            "PROMAC__LOGGING__UNSTRUCTURED__COLORIZE": "False",
            "PROMAC__SERVER__PORT": "35",
        },
    )

    helpers.print_struct(x, "collected_settings_dict")

    assert x == {
        "logging": {
            "level": "ERROR",
            "format": "whatever",
            "unstructured": {
                "colorize": False,
                "fmt": "lol",
            },
            "structured": {"custom_serializer": True},
        },
        "server": {
            "host": "hallo",
            "port": 35,
        },
        "and_so_on": "huy",
        "what": {
            "ever": "hallo",
        },
    }


# ==============================================================================
