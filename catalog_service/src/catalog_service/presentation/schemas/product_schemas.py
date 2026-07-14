from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    name: str = Field(max_length=128)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int | None
    name: str
    price: float
    stock: int
