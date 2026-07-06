import pytest

from order_service.domain.entities.order import Order, OrderStatus


@pytest.fixture
def order_item():
    return Order(user_id=1)


def test_add_item_recalculates_total(order_item):
    """Тестирование добавления предмета и пересчета стоимости"""
    result = order_item.add_item(product_id=1, quantity=1, price=5)

    assert result in order_item.items
    assert order_item.total == (result.price * result.quantity)


def test_cancel_changes_status_to_cancelled(order_item):
    """Тестирование отмены заказа"""
    order_item.cancel()

    assert order_item.status == OrderStatus.CANCELLED


def test_cancel_raises_error_if_paid(order_item):
    """Тестирование ошибки отмены заказа при статусе Оплачен"""
    order_item.status = OrderStatus.PAID

    with pytest.raises(ValueError):
        order_item.cancel()
