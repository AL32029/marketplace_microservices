from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    name: str
    price: float
    stock: int = 0

    id: Optional[int] = None

    def reduce_stock(self, quantity: int):
        if quantity <= 0:
            raise ValueError('The quantity must be positive')

        if quantity > self.stock:
            raise ValueError('The required quantity is missing from the warehouse')

        self.stock -= quantity

    def increase_stock(self, quantity: int):
        if quantity <= 0:
            raise ValueError('The quantity must be positive')

        self.stock += quantity
