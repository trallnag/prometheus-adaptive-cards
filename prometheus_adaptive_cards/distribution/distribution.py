"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Callable, Optional

from fastapi import Response
from loguru import logger
from requests import Session

from prometheus_adaptive_cards.config import Sending

from .model import Payload
from .utils import extract_url, requests_retry_session


def _handle_send_failure(
    url: str,
    session: Session = Session(),
    error_payload: Optional[dict] = None,
    notify_url: Optional[str] = None,
) -> Response:
    """
    Sends an optional dictionary to two optional targets.

    Used in case sending a templated alert payload to a configured target
    failed. In that case this function should be used to send an error info
    to either the same URL or a fallback URL.

    Args:
        error_payload (Optional[dict]): Payload that should be the body of the
            POST request made. If `None`, a GET will be performed instead.
        notify_url (Optional[str]): If not `None`, the request will be send
            to this URL. If `None`, `url` will be tried instead.
        url (str): Will be used if `notify_url` is `None`.
        session (Session, optional): Session to use for the request. Defaults
            to `Session()`.

    Returns:
        Response: Response for the request that handles send failure.
    """

    logger.info("Start to handle send failure.")

    if error_payload:
        method = "post"
        kwargs = {"url": notify_url if notify_url else url, "data": error_payload}
    else:
        method = "get"
        kwargs = {"url": notify_url if notify_url else url}

    response = getattr(session, method)(**kwargs)

    local_logger = logger.bind(
        url=url,
        notify_url=notify_url,
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
    error_parser: Optional[Callable[[dict], dict]] = None,
) -> list[Response]:
    logger.info("Start sending out payloads to targets.")

    session = requests_retry_session(
        retries=sending.retries, backoff_factor=sending.backoff_factor
    )

    responses = []

    for payload in payloads:
        local_logger = logger.bind(data=payload.data)
        for target in payload.targets:
            url = extract_url(target)
            if url:
                response = session.post(url, data=payload.data)

                responses.append(response)

                local_logger = local_logger.bind(
                    url=url,
                    status_code=response.status_code,
                    text=response.text,
                )

                if response.status_code < 300:
                    local_logger.info("Succeeded to sent payload to target.")
                else:
                    local_logger.error("Failed to send payload to target.")
                    if sending.notify_about_send_failure:
                        if error_parser:
                            response = _handle_send_failure(
                                error_payload=error_parser(
                                    {
                                        "response": {
                                            "description": "Info about the response for the request that contained the alert payload.",
                                            "status_code": response.status_code,
                                            "text": response.text,
                                            "request_url": response.request.url,
                                        },
                                        "sending": sending.dict(),
                                        "target": target.dict(),
                                        "payload_data": payload.data,
                                    },
                                ),
                                url=url,
                                notify_url=sending.notify_url,
                                session=session,
                            )
                            responses.append(response)
                        else:
                            response = _handle_send_failure(
                                error_payload=None,
                                url=url,
                                notify_url=sending.notify_url,
                                session=session,
                            )
                            responses.append(response)
            else:
                local_logger.warning("No target defined. Alert will not be send out.")
    return responses
