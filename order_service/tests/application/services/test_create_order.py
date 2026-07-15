from unittest.mock import AsyncMock

import pytest

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.infrastructure.repositories.sqlalchemy_order_repo import SQLAlchemyOrderRepo


@pytest.mark.asyncio
async def test_create_order_saves_order(order_item):
    """SQLAlchemyOrderRepo должен сохранять заказ в базе данных"""
    mock_repo = AsyncMock()
    mock_repo.save = AsyncMock()

    use_case = SQLAlchemyOrderRepo(mock_repo)

    await use_case.save(order_item)



@pytest.mark.asyncio
async def test_create_order_raises_if_stock_insufficient(order_item):
    """CreateOrderUseCase должен возвращать ValueError с ключевой фразов "insufficient stock" """
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