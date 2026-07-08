from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, ASGITransport

from catalog_service.domain.entities.product import Product
from catalog_service.main import app
from catalog_service.presentation.dependencies import get_all_products_use_case_depends


@pytest.mark.asyncio
async def test_get_product_stock():
    mock_use_case = AsyncMock()
    mock_use_case.get_all_products.return_value = [
        Product(id=1, name='Кофе', price=10, stock=50),
        Product(id=2, name='Молоко', price=3, stock=500),
        Product(id=3, name='Салфетки', price=3.5, stock=250),
    ]

    app.dependency_overrides[get_all_products_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.get(
            '/products'
        )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]['id'] == 1
    assert data[1]['name'] == 'Молоко'
    assert data[2]['price'] == 3.5
    assert data[0]['stock'] == 50

    mock_use_case.get_all_products.assert_called_once_with()

    app.dependency_overrides.clear()
