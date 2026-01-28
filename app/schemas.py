from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class SaleCreate(BaseModel):
    product_id: int = Field(ge=1)
    quantity: int = Field(ge=1)

class SaleOut(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    total: float
    remaining_stock: int
