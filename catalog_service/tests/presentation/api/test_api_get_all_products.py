import pytest
from dishka import Scope

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.domain.entities.product import Product


@pytest.fixture(scope='function')
async def create_product_use_case(test_container) -> CreateProductUseCase:
    async with test_container(scope=Scope.REQUEST) as request_container:
        return await request_container.get(CreateProductUseCase)


@pytest.fixture(scope='function')
def products():
    return [
        Product(name='Кофе', price=10, stock=50),
        Product(name='Молоко', price=3, stock=500),
        Product(name='Салфетки', price=3.5, stock=250),
    ]


@pytest.fixture(scope='function')
async def test_items(create_product_use_case, products):
    products_result = []

    for product in products:
        product_saved = await create_product_use_case.execute(product.name, product.price, product.stock)
        products_result.append(product_saved)

    return products_result


@pytest.mark.asyncio
async def test_get_product_stock(client, test_items):
    response = await client.get(
        '/products'
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]['id'] == test_items[0].id
    assert data[1]['name'] == test_items[1].name
    assert data[2]['price'] == test_items[2].price
    assert data[0]['stock'] == test_items[0].stock
