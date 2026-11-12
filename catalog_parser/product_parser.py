from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from bs4 import BeautifulSoup

from .http import fetch_html
from .products import Product
from .config import REQUEST_WORKERS


def parse_product_page(url):
    html = fetch_html(url)

    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")

    article = ""
    name = ""
    description = ""

    card = soup.find(class_="catalog-cards clearfix")
    if not card:
        print(f"[no card] {url}")
        return []

    main_info = card.find(class_="main-info")
    if not main_info:
            print(f"[no main-info] {url}")
            return []

    name_tag = main_info.find("h2")
    if name_tag:
        name = name_tag.get_text(" ", strip=True)

    table = main_info.find("table")

    if (table):
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if (len(cells)) < 2:
                continue

            label = cells[0].get_text(" ", strip=True).rstrip(" :").casefold()

            if "артикул" in label:
                article = cells[1].get_text(" ", strip=True).casefold()
                break

    if article:
        description_parts = []

        for p in card.find_all("p", recursive=False):
            text = p.get_text(" ", strip=True)

            if text:
                description_parts.append(text)

        description = " ".join(description_parts)

        return [Product(article, name, url, description)]
    
    line = card.find(class_="assortment-line")
    if not line:
        print("assortment-line not found")
        return []

    table = line.find("table")
    rows = table.find_all("tr")

    products = []

    name_ind = -1

    head = rows[0].find_all("td")
    texts_head = [t.get_text(" ", strip=True) for t in head]

    for ind in range(len(texts_head)):
        if texts_head[ind] == "наименование":
            name_ind = ind

    for row in rows[1:]:
        cells = row.find_all("td")
        texts = [cell.get_text(" ", strip=True) for cell in cells]

        article = texts[0].casefold()

        if name_ind == -1:
            name = name_tag.get_text(" ", strip=True)
        else:
            name = texts[name_ind]

        products.append(Product(article, name, url, description))

    return products


def collect_products_parallel(product_urls, workers=REQUEST_WORKERS):
    unique_products = {}
    lock = Lock()
    total = len(product_urls)

    def process_batch(urls_slice):
        local_results = []
        for url in urls_slice:
            res = parse_product_page(url)
            local_results.extend(res)
        return local_results

    if workers <= 1:
        for i, url in enumerate(product_urls, start=1):
            result = parse_product_page(url)
            
            with lock:
                for product in result:
                    key = product.article.strip().casefold()
                    if not key:
                        continue
                    
                    old = unique_products.get(key)
                    if old is None or len(product.description) > len(old.description):
                        unique_products[key] = product
                
        return unique_products

    chunk_size = max(1, total // (workers * 10))
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        current_chunk = []
        
        for i, url in enumerate(product_urls):
            current_chunk.append(url)
            if len(current_chunk) >= chunk_size or i == total - 1:
                futures.append(executor.submit(process_batch, current_chunk))
                current_chunk = []
                
        completed_count = 0
        for future in as_completed(futures):
            batch_results = future.result()
            completed_count += len(batch_results)
            
            with lock:
                for product in batch_results:
                    key = product.article.strip().casefold()
                    if not key:
                        continue
                        
                    old = unique_products.get(key)
                    if old is None:
                        unique_products[key] = product

    return unique_products
