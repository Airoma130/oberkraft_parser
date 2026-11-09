import csv
from pathlib import Path


def save_products(products, output_path="catalog_parser/data/products.csv"):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["article", "name", "url", "description"])

        for key in products:
            writer.writerow(products[key].to_row())