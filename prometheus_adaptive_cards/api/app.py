"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import base64
import pprint

from fastapi import FastAPI, Request

import prometheus_adaptive_cards.api.models as models
from prometheus_adaptive_cards.config.settings import Routing
from prometheus_adaptive_cards.preprocessing.actions import perform_actions
from prometheus_adaptive_cards.preprocessing.enhancement import enhance_data

# ==============================================================================


def create_fastapi_base() -> FastAPI:
    fastapi = FastAPI()

    @fastapi.get("/health")
    def health():
        return {"message": "OK", "symbol": "👌"}

    return fastapi


# ==============================================================================


def setup_routes(app: FastAPI, routing: Routing, route_prefix: str = "/route") -> FastAPI:
    for route in routing.routes:

        def route_handler(
            request: Request, data: models.Data, base64_encoded_webhook: str = ""
        ):
            # Performs actions (add, remove, etc.) on data based on config.
            perform_actions(routing, route, data)

            # Extract dynamic webhook from last part of path.
            if len(base64_encoded_webhook) > 0:
                route.webhooks.append(base64.b64decode(base64_encoded_webhook))

            data = enhance_data(request, data)

            print("data")
            pprint.pprint(data)
            print("base64_encoded_webhook")
            pprint.pprint(base64_encoded_webhook)

        route_postfix = r"{base64_encoded_webhook:path}" if route.catch else r""

        app.add_api_route(
            path=f"{route_prefix}/{route.name}/{route_postfix}",
            endpoint=route_handler,
            methods=["POST"],
        )

    return app
