from collections import deque

from bs4 import BeautifulSoup

from .http import fetch_html
from .utils import is_catalog, is_product, make_url


def bypass(start_url):
    queue = deque([start_url])
    visited = set()
    products = {}
    processed = 0
    

    while queue:

        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)
        processed += 1

        html = fetch_html(url)
        if html is None:
            continue

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all("a", href=True):
            link = make_url(tag["href"])

            if is_product(link):
                products[link] = {"url": link}

            elif is_catalog(link) and link not in visited:
                queue.append(link)

    return products
