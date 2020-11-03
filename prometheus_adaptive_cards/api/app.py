"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pprint

from fastapi import FastAPI, Request


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
            print("data")
            pprint.cpprint(data)
            print("base64_encoded_webhook")
            pprint.cpprint(base64_encoded_webhook)

        route_postfix = r"/{base64_encoded_webhook:path}" if route.catch else r""
        app.add_api_route(
            path=f"{route_prefix}/{route.name}{route_postfix}",
            endpoint=route_handler,
            methods=["POST"],
        )
    return app
