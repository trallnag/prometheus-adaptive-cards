"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Optional

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

from prometheus_adaptive_cards.config import Target

# ==============================================================================


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """[summary]

    Args:
        retries (int, optional): [description]. Defaults to 3.
        backoff_factor (float, optional): [description]. Defaults to 0.3.
        status_forcelist (tuple, optional): [description]. Defaults to (500, 502, 504).
        session ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]

    Licensing and attribution: Found [here](https://www.peterbe.com/plog/best-practice-with-retries-with-requests).
    No license. All attributions go to Peter Bengtsson.
    """

    session = session or requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# ==============================================================================


def extract_url(  # noqa: C901
    target: Target,
    common_labels: dict[str, str] = {},
    common_annotations: dict[str, str] = {},
) -> Optional[str]:
    """
    Goes through all target fields and tries to extract URL.

    1. expansion_url
    2. url_from_label
    3. url_from_annotation
    4. url

    Args:
        target (Target): Target object.
        common_labels (dict[str, str], optional): Common labels to use for
            expansion. Defaults to `{}`.
        common_annotations (dict[str, str], optional): Common annotations to
            use for expansion. Defaults to `{}`.

    Returns:
        Optional[str]: URL extracted from given `Target` object.
    """

    local_logger = logger.bind(
        target=target.dict(),
        common_labels=common_labels,
        common_annotations=common_annotations,
    )

    local_logger.debug("Start to extract url from target config and common attrs.")

    if target.expansion_url:
        try:
            return target.expansion_url.format(
                common_labels=common_labels, common_annotations=common_annotations
            )
        except KeyError:
            local_logger.opt(exception=True).error(
                "Expansion of given string failed. Continue with other options."
            )

    if target.url_from_label:
        try:
            return common_labels[target.url_from_label]
        except KeyError:
            local_logger.opt(exception=True).error(
                "Given label not found in common labels. Continue with other options."
            )

    if target.url_from_annotation:
        try:
            return common_annotations[target.url_from_annotation]
        except KeyError:
            local_logger.opt(exception=True).error(
                "Given annotation not found in common annotations. Continue with other options."
            )

    if target.url:
        return target.url

    local_logger.warning("No URL extracted.")

    return None


# ==============================================================================
