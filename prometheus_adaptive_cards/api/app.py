"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from fastapi import FastAPI


def create_fastapi_base() -> FastAPI:
    fastapi = FastAPI()

    @fastapi.get("/health")
    def health():
        return {"message": "OK", "symbol": "👌"}

    return fastapi
