from urllib.parse import urljoin, urlparse, urlunparse
from .config import DEFAULT_START_URL


def normalize_url(url):
    parsed = urlparse(url)

    path = parsed.path

    if path != "/" and path.endswith("/"):
        path = path[:-1]
    path = path.replace("//", "/")

    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        parsed.query,
        "",
    ))


def make_url(url):
    url = urljoin(DEFAULT_START_URL, url)
    return normalize_url(url)


def is_product(url):
    path = urlparse(url).path
    return path == "/products" or path.startswith("/products/")


def is_catalog(url):
    path = urlparse(url).path
    return path == "/catalog" or path.startswith("/catalog/")
