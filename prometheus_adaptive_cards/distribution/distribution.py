"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Callable, Optional

from fastapi import Response
from loguru import logger
from requests import Session

from prometheus_adaptive_cards.config import Sending, Target

from .model import Payload
from .utils import extract_url, requests_retry_session


def _handle_send_failure(
    error_payload: Optional[dict],
    fallback_url: Optional[str],
    url: str,
    session: Session = Session(),
) -> Response:
    """
    Sends an optional dictionary to two optional targets.

    Used in case sending a templated alert payload to a configured target
    failed. In that case this function should be used to send an error info
    to either the same URL or a fallback URL.

    Args:
        error_payload (Optional[dict]): Payload that should be the body of the
            POST request made. If `None`, a GET will be performed instead.
        fallback_url (Optional[str]): If not `None`, the request will be send
            to this URL. If `None`, `url` will be tried instead.
        url (str): Will be used if `fallback_url` is `None`.
        session (Session, optional): Session to use for the request. Defaults
            to `Session()`.
    """

    logger.info("Start to handle send failure.")

    if error_payload:
        method = "post"
        kwargs = {"url": fallback_url if fallback_url else url, "data": error_payload}
    else:
        method = "get"
        kwargs = {"url": fallback_url if fallback_url else url}

    response = getattr(session, method)(**kwargs)

    local_logger = logger.bind(
        url=url,
        fallback_url=fallback_url,
        error_payload=error_payload,
        status_code=response.status_code,
        text=response.text,
    )

    if response.status_code < 300:
        local_logger.info("Succeeded sending send failure info.")
    else:
        local_logger.error("Failed sending send failure info.")

    return response


def send(
    payloads: list[Payload],
    sending: Sending,
    error_parser: Optional[Callable[[Response, Sending, Target, Payload], dict]] = None,
):
    logger.info("Start sending out payloads to targets.")

    session = requests_retry_session(
        retries=sending.retries, backoff_factor=sending.backoff_factor
    )

    for payload in payloads:
        local_logger = logger.bind(data=payload.data)
        for target in payload.targets:
            url = extract_url(target)
            response = session.post(url, data=payload.data)

            local_logger = logger.bind(
                url=url,
                status_code=response.status_code,
                text=response.text,
            )

            if response.status_code < 300:
                local_logger.info("Succeeded to sent payload to target.")
            else:
                local_logger.error("Failed to send payload to target.")
                if sending.handle_send_failure:
                    if error_parser:
                        _handle_send_failure(
                            error_payload=error_parser(
                                response,
                                sending,
                                target,
                                payload,
                            ),
                            url=url,
                            fallback_url=sending.fallback_url,
                            session=session,
                        )
                    else:
                        _handle_send_failure(
                            url=url,
                            fallback_url=sending.fallback_url,
                            session=session,
                        )
