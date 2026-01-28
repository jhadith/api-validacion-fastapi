from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

class InMemoryDB:
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._next_product_id = 1
        self._next_sale_id = 1

    def reset(self) -> None:
        self._products.clear()
        self._next_product_id = 1
        self._next_sale_id = 1

    def create_product(self, name: str, price: float, stock: int) -> Product:
        pid = self._next_product_id
        self._next_product_id += 1
        product = Product(id=pid, name=name, price=price, stock=stock)
        self._products[pid] = product
        return product

    def get_product(self, product_id: int) -> Product | None:
        return self._products.get(product_id)

    def update_product(self, product_id: int, name: str | None, price: float | None, stock: int | None) -> Product | None:
        product = self._products.get(product_id)
        if product is None:
            return None
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock
        return product

    def delete_product(self, product_id: int) -> bool:
        return self._products.pop(product_id, None) is not None

    def next_sale_id(self) -> int:
        sid = self._next_sale_id
        self._next_sale_id += 1
        return sid
