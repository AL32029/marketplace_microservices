import pytest

from order_service.domain.entities.order import Order, OrderStatus
from order_service.domain.exceptions.catalog_errors import OrderWasPayedError


def test_add_item_recalculates_total():
    """Order должен добавлять OrderItem и делать пересчет total"""
    order = Order(user_id=1)
    result = order.add_item(product_id=1, quantity=1, price=5)

    assert result in order.items
    assert order.total == (result.price * result.quantity)


def test_cancel_changes_status_to_cancelled():
    """Order должен присваивать status OrderStatus.CANCELLED"""
    order = Order(user_id=1)
    order.cancel()

    assert order.status == OrderStatus.CANCELLED


def test_cancel_raises_error_if_paid():
    """Order должен выдавать OrderWasPayedError при статусе OrderStatus.PAID"""
    order = Order(user_id=1)
    order.status = OrderStatus.PAID

    with pytest.raises(OrderWasPayedError):
        order.cancel()
