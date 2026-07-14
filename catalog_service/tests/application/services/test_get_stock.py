from unittest.mock import AsyncMock

import pytest

from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.domain.entities.product import Product
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError


@pytest.mark.asyncio
async def test_get_stock():
    """GetStockUseCase должен получить продукт из базы данных и вернуть количество остатков"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Product(
        id=1,
        name='Вода дистиллированная',
        price=50,
        stock=0
    )

    use_case = GetStockUseCase(mock_repo)

    stock = await use_case.get_stock(1)

    mock_repo.get_by_id.assert_called_once()

    assert stock == 0


@pytest.mark.asyncio
async def test_get_stock_error_not_found():
    """GetStockUseCase должен вернуть ошибку ProductNotFoundError"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None

    use_case = GetStockUseCase(mock_repo)

    with pytest.raises(ProductNotFoundError) as e:
        await use_case.get_stock(1)

        assert e.value == 'Product with ID 1 not found'

    mock_repo.get_by_id.assert_called_once()
