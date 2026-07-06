from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
