from fastapi import FastAPI, HTTPException, status
from .schemas import ProductCreate, ProductUpdate, ProductOut, SaleCreate, SaleOut
from .storage import InMemoryDB
from .services import register_sale, BusinessRuleError

app = FastAPI(title="API Inventario y Ventas", version="1.0.0")

db = InMemoryDB()

@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate):
    product = db.create_product(payload.name, payload.price, payload.stock)
    return product

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return product

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate):
    product = db.update_product(product_id, payload.name, payload.price, payload.stock)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    ok = db.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return

@app.post("/sales", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sale(payload: SaleCreate):
    try:
        result = register_sale(db, payload.product_id, payload.quantity)
        return result
    except BusinessRuleError as e:
        raise HTTPException(status_code=409, detail=str(e))
