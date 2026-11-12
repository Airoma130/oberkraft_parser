import time
import threading
import requests
from .config import REQUEST_DELAY, REQUEST_TIMEOUT

thread_local = threading.local()


def get_session():
    session = getattr(thread_local, "session", None)
    
    if session is None:
        session = requests.Session()
        thread_local.session = session
        
    return session


def fetch_html(url, delay=REQUEST_DELAY):
    if delay > 0:
        time.sleep(delay)

    try:
        response = get_session().get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        if response.status_code != 200:
            print(f"[skip] {url} -> {response.status_code}")
            return None

        return response.text

    except requests.RequestException as exc:
        print(f"[error] {url}: {exc}")
        return None
