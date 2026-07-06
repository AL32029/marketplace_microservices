from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class OrderStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PAID = 'paid'
    CANCELLED = 'cancelled'


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    price: float


@dataclass
class Order:
    user_id: int

    id: Optional[int] = None
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    total: float = 0.0

    def add_item(self, product_id: int, quantity: int, price: float):
        if quantity <= 0:
            raise ValueError('The quantity must be positive')

        if price < 0:
            raise ValueError('The price should not be negative')

        new_item = OrderItem(
            product_id=product_id,
            quantity=quantity,
            price=price
        )

        self.items.append(new_item)
        self.total = sum([item.price * item.quantity for item in self.items])

        return new_item

    def cancel(self):
        if self.status == OrderStatus.PAID:
            raise ValueError('The order has been paid for, cancellation is not possible')

        self.status = OrderStatus.CANCELLED
