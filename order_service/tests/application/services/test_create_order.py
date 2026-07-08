from unittest.mock import AsyncMock

import pytest

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.tests.application.services.conftest import order_repo, order_item


@pytest.mark.asyncio
async def test_create_order_saves_order(order_repo, order_item):
    """Тестирование сохранения заказа"""
    await order_repo.save(order_item)
    assert order_item.id is not None


@pytest.mark.asyncio
async def test_create_order_raises_if_stock_insufficient(order_item):
    """Тестирование отсутствия нужного количества товара на складе"""
    mock_repo = AsyncMock()
    mock_catalog = AsyncMock()
    mock_catalog.check_stock.return_value = False

    use_case = CreateOrderUseCase(mock_repo, mock_catalog)

    with pytest.raises(ValueError, match="insufficient stock"):
        await use_case.execute(
            user_id=order_item.user_id,
            items=order_item.items
        )

    mock_repo.save.assert_not_called()