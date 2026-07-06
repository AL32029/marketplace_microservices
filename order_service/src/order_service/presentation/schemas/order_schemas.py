from typing import List

from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int
    price: float


class CreateOrderRequest(BaseModel):
    user_id: int
    items: List[OrderItemRequest]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: List[OrderItemResponse]
    status: str
    total: float
