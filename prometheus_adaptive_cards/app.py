"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import base64

from fastapi import FastAPI

from .config import Routing, Target
from .distribution import send
from .model import AlertGroup
from .preprocessing import preprocess

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

        # ----------------------------------------------------------------------

        def route_handler(alert_group: AlertGroup, b64_webhook: str = ""):
            route.targets.append(Target.construct(url=base64.b64decode(b64_webhook)))

            responses = []

            enhanced_alert_groups = preprocess(routing, route, alert_group)

            for enhanced_alert_group in enhanced_alert_groups:
                payloads, error_parser = template(enhanced_alert_group)
                
                responses.append(
                    send(
                        payloads=payloads,
                        sending=route.sending or routing.sending,
                        error_parser=error_parser,
                    )
                )

        # ----------------------------------------------------------------------

        route_postfix = r"{b64_webhook:path}" if route.catch else r""

        app.add_api_route(
            path=f"{route_prefix}/{route.name}/{route_postfix}",
            endpoint=route_handler,
            methods=["POST"],
        )

    return app
