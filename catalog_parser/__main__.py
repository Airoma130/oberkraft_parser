from .config import DEFAULT_START_URL
from .bypass import bypass
from .product_parser import extract_data_from_products
from .storage import save_products


def main():
    products = bypass(
        DEFAULT_START_URL,
    )

    all_products = extract_data_from_products(products)

    save_products(all_products)


if __name__ == "__main__":
    main()