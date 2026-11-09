import time
import requests
from .config import REQUEST_DELAY, REQUEST_TIMEOUT


def fetch_html(url, delay=REQUEST_DELAY):
    if delay > 0:
        time.sleep(delay)

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            print(f"[skip] {url} -> {response.status_code}")
            return None

        return response.text

    except requests.RequestException as exc:
        print(f"[error] {url}: {exc}")
        return None
