"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import base64

from fastapi import FastAPI

from .config import Routing, Target
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

            enhanced_alert_groups = preprocess(routing, route, alert_group)
            for enhanced_alert_group in enhanced_alert_groups:
                # payloads = template(enhanced_alert_group)
                # send(payloads)
                pass

            # for alert_group in preprocess(routing, route, body):
            #     if len(base64_webhook) > 0:
            #         route.webhooks.append(base64.b64decode(base64_webhook))

            #     print("alert_group")
            #     pprint.pprint(alert_group)
            #     print("base64_encoded_webhook")
            #     pprint.pprint(base64_webhook)

        # ----------------------------------------------------------------------

        route_postfix = r"{b64_webhook:path}" if route.catch else r""

        app.add_api_route(
            path=f"{route_prefix}/{route.name}/{route_postfix}",
            endpoint=route_handler,
            methods=["POST"],
        )

    return app
