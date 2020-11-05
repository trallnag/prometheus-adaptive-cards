"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Pattern

import pytest
from pydantic import ValidationError, parse_obj_as

import prometheus_adaptive_cards.config.settings as settings

# ==============================================================================


def test_structured_valid(helpers):
    x = parse_obj_as(
        settings.Structured, {"custom_serializer": True, "does_not_exist": 1}
    )
    helpers.print_struct(x)
    assert x.custom_serializer is True
    with pytest.raises(AttributeError):
        assert x.does_not_exist == 1


def test_structured_invalid():
    with pytest.raises(ValidationError):
        _ = parse_obj_as(settings.Structured, {"custom_serializer": {"lul": 21}})


def test_unstructured_valid(helpers):
    x = parse_obj_as(settings.Unstructured, {"colorize": True})
    helpers.print_struct(x)
    assert x.colorize is True


def test_logging(helpers):
    x = parse_obj_as(
        settings.Logging, {"level": "ERROR", "structured": {"custom_serializer": True}}
    )
    helpers.print_struct(x)
    assert x.level == "ERROR"
    assert x.unstructured.colorize is True
    assert x.structured.custom_serializer is True


# ==============================================================================


def test_server():
    x = parse_obj_as(settings.Server, {})
    assert x.host == "127.0.0.1"
    assert x.port == 8000


# ==============================================================================


def test_remove_valid_without_re(helpers):
    x = parse_obj_as(
        settings.Remove,
        {
            "annotations": ["whatever", "annotation_name"],
            "labels": ["alertname", "__whatevers"],
        },
    )
    helpers.print_struct(x)
    assert len(x.annotations) == 2
    assert len(x.labels) == 2


def test_remove_valid_without_re_with_casting(helpers):
    x = parse_obj_as(
        settings.Remove,
        {
            "annotations": ["whatever", 1],
            "labels": ["alertname", "__whatevers"],
        },
    )
    helpers.print_struct(x)
    assert len(x.annotations) == 2
    assert isinstance(x.annotations[1], str)
    assert len(x.labels) == 2


def test_remove_invalid_without_re():
    with pytest.raises(ValidationError):
        _ = parse_obj_as(
            settings.Remove,
            {
                "annotations": ["whatever", {"complex": 32423}],
                "labels": ["alertname", "__whatevers"],
            },
        )


def test_remove_valid_re(helpers):
    x = parse_obj_as(
        settings.Remove,
        {
            "re_annotations": ["(.*)"],
        },
    )
    helpers.print_struct(x)
    assert isinstance(x.re_annotations[0], Pattern)


# ==============================================================================


def test_add_valid(helpers):
    x = parse_obj_as(
        settings.Add,
        {
            "annotations": {
                "foo": "bar",
                "fooom": "lol",
            }
        },
    )
    helpers.print_struct(x)
    assert isinstance(x.annotations, dict)
    assert len(x.annotations) == 2
    assert x.annotations["foo"] == "bar"
    with pytest.raises(AttributeError):
        x.annotations.foo == "bar"


def test_override_valid(helpers):
    x = parse_obj_as(
        settings.Override,
        {
            "annotations": {
                "foo": "bar",
                "fooom": "lol",
            }
        },
    )
    helpers.print_struct(x)
    assert isinstance(x.annotations, dict)
    assert len(x.annotations) == 2
    assert x.annotations["foo"] == "bar"
    with pytest.raises(AttributeError):
        x.annotations.foo == "bar"


def test_route_invalid_name():
    with pytest.raises(ValidationError):
        _ = parse_obj_as(
            settings.Route,
            {"name": "HALLO ROUTE"},
        )


def test_route_valid(helpers):
    x = parse_obj_as(
        settings.Route,
        {
            "name": "generic_fefef-fef",
            "add": {"labels": {"new": "label"}},
            "remove": {"annotations": ["foo", "bar"]},
            "webhooks": ["https://www.googleapis.com/"],
        },
    )
    helpers.print_struct(x)
    assert x.name == "generic_fefef-fef"
    assert x.add.labels["new"] == "label"
    assert x.remove.annotations[1] == "bar"
    assert len(x.webhooks) == 1


def test_routing(helpers):
    x = parse_obj_as(
        settings.Routing,
        {
            "add": {"labels": {"new": "label"}},
            "remove": {"annotations": ["foo", "bar"]},
            "routes": [
                {
                    "name": "generic_fefef",
                    "remove": {"annotations": ["foo", "bar"]},
                },
                {
                    "name": "generic_fefef-fef",
                    "webhooks": ["https://www.googleapis.com/"],
                },
            ],
        },
    )
    helpers.print_struct(x)
    assert x.add.labels["new"] == "label"
    assert x.remove.annotations[1] == "bar"
    assert x.routes[0].remove.annotations[1] == "bar"


def test_routing_invalid_non_unique_route_names():
    with pytest.raises(ValidationError):
        _ = parse_obj_as(
            settings.Routing,
            {
                "routes": [
                    {
                        "name": "generic_fefef",
                        "remove": {"annotations": ["foo", "bar"]},
                    },
                    {
                        "name": "generic_fefef",
                        "webhooks": ["https://www.googleapis.com/"],
                    },
                ]
            },
        )


def test_settings_empty(helpers):
    x = parse_obj_as(settings.Settings, {})
    helpers.print_struct(x)
    assert x.logging.level == "INFO"
    assert x.routing.add.annotations == {}


# ==============================================================================
# route


def test_route_invalid_split_by_both():
    with pytest.raises(ValidationError):
        _ = parse_obj_as(
            settings.Route,
            {
                "name": "name",
                "split_by_label": "test",
                "split_by_annotation": "test",
            },
        )


def test_route_valid_split_by():
    x = parse_obj_as(
        settings.Route,
        {
            "name": "name",
            "split_by_label": "test",
        },
    )
    assert x.split_by_label == "test"
    assert x.split_by_annotation is None


# ==============================================================================


def test_settings_singleton_valid_defaults_only(helpers):
    x = settings.settings_singleton(refresh=True, cli_args=["--config_file", "/"])

    helpers.print_struct(x.dict(), "Settings object")

    assert x.logging.level == "INFO"
    assert x.routing.add.annotations == {}
    assert x.routing.routes[0].name == "generic"


def test_settings_singleton_valid_with_env_vars(helpers):
    x = settings.settings_singleton(
        refresh=True,
        env={
            "WHATEVER": "ffefe",
            "PROMAC__SERVER__PORT": 1,
            "PROMAC__LOGGING__UNSTRUCTURED__COLORIZE": "false",
        },
        cli_args=["--config_file", "/"],
    )
    helpers.print_struct(x.dict(), "Settings object")
    assert x.logging.unstructured.colorize is False
    assert x.server.port == 1


def test_settings_singleton_valid_with_cli_args(helpers):
    x = settings.settings_singleton(
        refresh=True,
        cli_args=[
            "--config_file",
            "/",
            "--logging.level",
            "ERROR",
            "--server.port",
            "12",
        ],
    )
    helpers.print_struct(x.dict(), "Settings object")
    assert x.logging.level == "ERROR"
    assert x.server.port == 12


def test_settings_singleton_valid_with_cli_args_and_env(helpers):
    x = settings.settings_singleton(
        refresh=True,
        cli_args=[
            "--config_file",
            "/",
            "--logging.level",
            "ERROR",
            "--server.port",
            "12",
        ],
        env={"PROMAC__LOGGING__LEVEL": "DEBUG", "PROMAC__SERVER__PORT": "55"},
    )
    helpers.print_struct(x.dict(), "Settings object")
    assert x.logging.level == "ERROR"
    assert x.server.port == 12


def test_settings_singleton_big_example(helpers, tmp_path):
    file_content = """\
    logging:
      level: DEBUG
      format: unstructured
      unstructured:
        colorize: false
    server:
      port: 36969
    routing:
      remove:
        labels:
          - test
          - more
      routes:
        - name: route1
          webhooks:
            - https://www.google.com
            - https://www.google.com
        - name: route2
    """

    file_path = tmp_path / "file.yml"
    file_path.write_text(file_content)

    x = settings.settings_singleton(
        refresh=True,
        cli_args=[
            "--config_file",
            str(file_path.resolve()),
            "--server.port",
            "12",
        ],
        env={"PROMAC__LOGGING__LEVEL": "ERROR", "PROMAC__SERVER__PORT": "55"},
    )
    helpers.print_struct(x.dict(), "Settings object")

    assert x.logging.level == "ERROR"
    assert x.server.port == 12
    assert len(x.routing.routes) == 3


# ==============================================================================


def test_ensure_generic_route_exists():
    x = settings.settings_singleton(refresh=True)
    settings._ensure_generic_route_exists(x)

    assert x.routing.routes[0].name == "generic"
    assert len(x.routing.routes) == 1


def test_ensure_generic_route_exists_skip(tmp_path):
    file_content = """\
    routing:
      routes:
        - name: generic
    """

    file_path = tmp_path / "file.yml"
    file_path.write_text(file_content)

    x = settings.settings_singleton(
        refresh=True,
        cli_args=[
            "--config_file",
            str(file_path.resolve()),
        ],
    )

    x = settings.settings_singleton(refresh=True)
    settings._ensure_generic_route_exists(x)

    assert x.routing.routes[0].name == "generic"
    assert len(x.routing.routes) == 1


# ==============================================================================
