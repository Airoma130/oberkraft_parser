from .config import DEFAULT_START_URL
from .bypass import bypass
from .product_parser import collect_products_parallel
from .storage import save_products


def main():
    products = bypass(
        DEFAULT_START_URL,
    )

    products_urls = list(products.keys())

    all_products = collect_products_parallel(products_urls)

    save_products(all_products)


if __name__ == "__main__":
    main()