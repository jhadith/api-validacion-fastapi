import pytest
from app.storage import InMemoryDB
from app.services import (
    BusinessRuleError,
    calculate_total,
    validate_stock_available,
    register_sale
)

def test_calculate_total_ok():
    assert calculate_total(1.25, 3) == 3.75

def test_calculate_total_rejects_non_positive_price():
    with pytest.raises(BusinessRuleError):
        calculate_total(0, 2)

def test_calculate_total_rejects_non_positive_quantity():
    with pytest.raises(BusinessRuleError):
        calculate_total(2.0, 0)

def test_register_sale_product_not_found():
    db = InMemoryDB()
    with pytest.raises(BusinessRuleError):
        register_sale(db, product_id=999, quantity=1)

def test_register_sale_ok_and_stock_decreases():
    db = InMemoryDB()
    p = db.create_product("Coca Cola 1L", 1.25, 10)

    result = register_sale(db, product_id=p.id, quantity=3)

    assert result["product_id"] == p.id
    assert result["quantity"] == 3
    assert result["total"] == 3.75
    assert result["remaining_stock"] == 7

    # Verifica que el producto en DB también quedó con stock actualizado
    updated = db.get_product(p.id)
    assert updated is not None
    assert updated.stock == 7

def test_register_sale_rejects_insufficient_stock():
    db = InMemoryDB()
    p = db.create_product("Coca Cola 1L", 1.25, 2)

    with pytest.raises(BusinessRuleError) as e:
        register_sale(db, product_id=p.id, quantity=3)

    assert "Stock insuficiente" in str(e.value)

def test_validate_stock_available_rejects_zero_or_negative_quantity():
    db = InMemoryDB()
    p = db.create_product("Test", 1.0, 10)

    with pytest.raises(BusinessRuleError):
        validate_stock_available(p, 0)

    with pytest.raises(BusinessRuleError):
        validate_stock_available(p, -1)
