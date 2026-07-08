from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, ASGITransport

from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError
from catalog_service.main import app
from catalog_service.presentation.dependencies import get_stock_use_case_depends


@pytest.mark.asyncio
async def test_get_product_stock():
    mock_use_case = AsyncMock()
    mock_use_case.get_stock.return_value = 500

    app.dependency_overrides[get_stock_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.get(
            '/products/1/stock'
        )

    assert response.status_code == 200
    data = response.json()
    assert 'stock' in data
    assert data['stock'] == 500

    mock_use_case.get_stock.assert_called_once_with(1)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_product_stock_error_not_found():
    mock_use_case = AsyncMock()
    mock_use_case.get_stock.side_effect = ProductNotFoundError('Товар не найден')

    app.dependency_overrides[get_stock_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.get(
            '/products/50/stock'
        )

    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'Товар не найден' in data['detail']

    mock_use_case.get_stock.assert_called_once_with(50)

    app.dependency_overrides.clear()
