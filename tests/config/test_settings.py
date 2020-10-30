
"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""


import prometheus_adaptive_cards.config.settings as settings
import pytest


# ==============================================================================
# parse_args


def test_parse_args():
    args = ["--config_file", "foo/bar.yml"]
    args = settings._parse_args(args)
    assert args.config_file == "foo/bar.yml"
    assert getattr(args, "does_not_exist", None) is None


def test_parse_nothing():
    args = []
    args = settings._parse_args(args)
    assert getattr(args, "does_not_exist", None) is None


# ==============================================================================
# parse_files


def test_parse_files_no_files():
    assert settings._parse_files(force_file="/does_not_exist/", lookup_override=[]) == {}


def test_parse_files_force_file(tmp_path):
    force_file = tmp_path / "force_file.yml"
    force_file.write_text("a: b")

    normal_file = tmp_path / "normal_file.yml"
    normal_file.write_text("a: c")

    dct = settings._parse_files(force_file=str(force_file.resolve()), lookup_override=[str(normal_file.resolve())])
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

    dct = settings._parse_files(lookup_override=files)
    assert dct["a"] == "d"
    assert dct["foo"] == "bar"


def test_parse_files_local(tmp_path):
    n1 = tmp_path / "n1.yml"
    n1.write_text("a: c\ntrol: sa")

    (tmp_path / "n1.local.yml").write_text("a: b\nfoo: bar")

    dct = settings._parse_files(lookup_override=[str(n1.resolve())])
    assert dct["a"] == "b"
    assert dct["foo"] == "bar"
    assert dct["trol"] == "sa"
