import pytest

from order_service.domain.entities.order import Order, OrderStatus


def test_add_item_recalculates_total():
    """Тестирование добавления предмета и пересчета стоимости"""
    order = Order(user_id=1)
    result = order.add_item(product_id=1, quantity=1, price=5)

    assert result in order.items
    assert order.total == (result.price * result.quantity)


def test_cancel_changes_status_to_cancelled():
    """Тестирование отмены заказа"""
    order = Order(user_id=1)
    order.cancel()

    assert order.status == OrderStatus.CANCELLED


def test_cancel_raises_error_if_paid():
    """Тестирование ошибки отмены заказа при статусе Оплачен"""
    order = Order(user_id=1)
    order.status = OrderStatus.PAID

    with pytest.raises(ValueError):
        order.cancel()
