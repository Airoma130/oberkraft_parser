from bs4 import BeautifulSoup

from .http import fetch_html
from .products import Product


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


def extract_data_from_products(products):
    all_products = {}

    for url in products:
        result = parse_product_page(url)

        for prod in result:
            key = prod.article.strip().casefold()

            if not key:
                continue

            old = all_products.get(key)

            if old is None:
                all_products[key] = prod

    return all_products
