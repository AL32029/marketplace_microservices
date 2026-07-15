from unittest.mock import AsyncMock

import pytest

from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.domain.entities.product import Product
from catalog_service.domain.exceptions.catalog_errors import (
    InsufficientStockError,
    NegativeQuantityError,
    ProductNotFoundError,
)


@pytest.mark.asyncio
async def test_reserve_stock():
    """ReserveStockUseCase должен забронировать 20 единиц товара на складе и сохранить изменения в базе данных"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Product(
        id=1,
        name='Вода дистиллированная',
        price=50,
        stock=20
    )

    use_case = ReserveStockUseCase(mock_repo)

    await use_case.reserve_stock(1, 20)

    mock_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_stock_error_not_found():
    """ReserveStockUseCase должен вернуть ошибку ProductNotFoundError"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None

    use_case = ReserveStockUseCase(mock_repo)

    with pytest.raises(ProductNotFoundError) as e:
        await use_case.reserve_stock(1, 20)

    assert str(e.value) == 'Product with ID 1 not found'

    mock_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_stock_error_insufficient_stock_error():
    """ReserveStockUseCase должен вернуть ошибку InsufficientStockError"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Product(
        id=1,
        name='Вода дистиллированная',
        price=50,
        stock=19
    )

    use_case = ReserveStockUseCase(mock_repo)

    with pytest.raises(InsufficientStockError) as e:
        await use_case.reserve_stock(1, 20)

        assert str(e.value) == 'The required quantity is missing from the warehouse'

    mock_repo.get_by_id.assert_called_once()


@pytest.mark.asyncio
async def test_get_stock_error_negative_quantity_error():
    """ReserveStockUseCase должен вернуть ошибку NegativeQuantityError"""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Product(
        id=1,
        name='Вода дистиллированная',
        price=50,
        stock=19
    )

    use_case = ReserveStockUseCase(mock_repo)

    with pytest.raises(NegativeQuantityError) as e:
        await use_case.reserve_stock(1, -10)

        assert str(e.value) == 'The quantity must be positive'

    mock_repo.get_by_id.assert_called_once()
