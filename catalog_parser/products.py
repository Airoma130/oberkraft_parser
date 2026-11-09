from dataclasses import dataclass


@dataclass
class Product:
    article: str
    name: str = ""
    description: str = ""
    url: str = ""

    def to_row(self):
        return [
            self.article,
            self.name,
            self.url,
            self.description,
        ]