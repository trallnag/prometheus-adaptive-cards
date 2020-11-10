import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry


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

    Usage Example:

    ```python
    response = requests_retry_session().get('https://www.peterbe.com/')
    print(response.status_code)

    s = requests.Session()
    s.auth = ('user', 'pass')
    s.headers.update({'x-test': 'true'})

    response = requests_retry_session(session=s).get(
        'https://www.peterbe.com'
    )
    ```

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
