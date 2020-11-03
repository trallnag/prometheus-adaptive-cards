"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pytest
from fastapi import FastAPI

import prometheus_adaptive_cards.api.app as app
from prometheus_adaptive_cards.config.settings import Route, Routing


def test_setup_routes_number_of_routes():
    fastapi_app = app.setup_routes(
        app=FastAPI(),
        routing=Routing(
            routes=[
                Route(name="route1"),
                Route(name="route2"),
                Route(name="route3"),
            ]
        ),
    )
    assert (
        len(
            [
                route.path
                for route in fastapi_app.routes
                if route.path.startswith("/route")
            ]
        )
        == 3
    )

    fastapi_app = app.setup_routes(
        app=FastAPI(),
        routing=Routing(
            routes=[
                Route(name="route1"),
                Route(name="route2"),
            ]
        ),
    )
    assert (
        len(
            [
                route.path
                for route in fastapi_app.routes
                if route.path.startswith("/route")
            ]
        )
        == 2
    )

    with pytest.raises(Exception):
        fastapi_app = app.setup_routes(
            app=FastAPI(),
            routing=Routing(
                routes=[
                    Route(name="route1"),
                    Route(name="route1"),
                ]
            ),
        )
        assert (
            len(
                [
                    route.path
                    for route in fastapi_app.routes
                    if route.path.startswith("/route")
                ]
            )
            == 2
        )
