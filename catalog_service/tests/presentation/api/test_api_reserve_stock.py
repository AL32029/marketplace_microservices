from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, ASGITransport

from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError
from catalog_service.main import app
from catalog_service.presentation.dependencies import reserve_stock_use_case_depends


@pytest.mark.asyncio
async def test_reserve_stock():
    mock_use_case = AsyncMock()
    mock_use_case.reserve_stock.return_value = None

    app.dependency_overrides[reserve_stock_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.post(
            '/products/1/reserve',
            params={'quantity': 50}
        )

    assert response.status_code == 200
    data = response.json()
    assert 'success' in data
    assert data['success'] == True

    mock_use_case.reserve_stock.assert_called_once_with(1, 50)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_reserve_stock_error_not_found():
    mock_use_case = AsyncMock()
    mock_use_case.reserve_stock.side_effect = ProductNotFoundError('Товар не найден')

    app.dependency_overrides[reserve_stock_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.post(
            '/products/50/reserve',
            params={'quantity': 50}
        )

    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'Товар не найден' in data['detail']

    mock_use_case.reserve_stock.assert_called_once_with(50, 50)

    app.dependency_overrides.clear()
