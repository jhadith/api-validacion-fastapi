from .storage import InMemoryDB, Product

class BusinessRuleError(Exception):
    pass

def validate_stock_available(product: Product, quantity: int) -> None:
    if quantity <= 0:
        raise BusinessRuleError("La cantidad debe ser mayor a cero.")
    if product.stock < quantity:
        raise BusinessRuleError("Stock insuficiente para completar la venta.")

def calculate_total(price: float, quantity: int) -> float:
    if price <= 0:
        raise BusinessRuleError("El precio debe ser mayor a cero.")
    if quantity <= 0:
        raise BusinessRuleError("La cantidad debe ser mayor a cero.")
    return round(price * quantity, 2)

def register_sale(db: InMemoryDB, product_id: int, quantity: int) -> dict:
    product = db.get_product(product_id)
    if product is None:
        raise BusinessRuleError("Producto no encontrado.")

    validate_stock_available(product, quantity)
    total = calculate_total(product.price, quantity)

    product.stock -= quantity
    sale_id = db.next_sale_id()

    return {
        "sale_id": sale_id,
        "product_id": product.id,
        "quantity": quantity,
        "total": total,
        "remaining_stock": product.stock
    }
