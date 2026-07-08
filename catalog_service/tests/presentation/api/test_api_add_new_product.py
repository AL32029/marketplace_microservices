from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient, ASGITransport

from catalog_service.domain.entities.product import Product
from catalog_service.main import app
from catalog_service.presentation.dependencies import create_product_use_case_depends


@pytest.mark.asyncio
async def test_add_new_item():
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = Product(id=1, name='Кофе', price=10, stock=50)

    app.dependency_overrides[create_product_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.post(
            '/products',
            json={'name': 'Кофе', 'price': 10, 'stock': 50}
        )

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'Кофе'
    assert data['price'] == 10
    assert data['stock'] == 50

    mock_use_case.execute.assert_called_once_with('Кофе', 10, 50)

    app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'name,price,stock',
    [
        ['Кофе', -10, 50],
        ['Кофе', 50, -10],
        ['Кофе', -10, -50],
        [
            'КофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофеКофе',
            10, 50
        ],
    ]
)
async def test_add_new_item_validation_error(name, price, stock):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test'
    ) as client:
        response = await client.post(
            '/products',
            json={'name': name, 'price': price, 'stock': stock}
        )

    assert response.status_code == 422
