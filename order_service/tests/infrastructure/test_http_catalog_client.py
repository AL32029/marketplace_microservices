import httpx
import pytest

from order_service.domain.entities.order import OrderItem
from order_service.domain.exceptions.catalog_errors import ProductNotFoundError, CatalogUnavailableError
from order_service.infrastructure.clients.http_catalog_client import HTTPCatalogClient


@pytest.fixture
def catalog_client():
    return HTTPCatalogClient(base_url='http://test.local')


@pytest.fixture
def order_item():
    return OrderItem(product_id=1, quantity=5, price=10.0)


@pytest.mark.asyncio
async def test_check_stock_returns_true_if_stock_sufficient(catalog_client, order_item, httpx_mock):
    """Тестирование выполнения эндпоинта GET /products/{product_id}/stock при наличии требуемого количества товара"""
    httpx_mock.add_response(
        method='GET',
        url=f'http://test.local/products/{order_item.product_id}/stock',
        json={'stock': 5},
        status_code=200
    )

    stock_sufficient = await catalog_client.check_stock(product_id=order_item.product_id, quantity=order_item.quantity)

    assert stock_sufficient


@pytest.mark.asyncio
async def test_check_stock_returns_false_if_stock_insufficient(catalog_client, order_item, httpx_mock):
    """Тестирование выполнения эндпоинта GET /products/{product_id}/stock при отсутствии требуемого количества товара"""
    httpx_mock.add_response(
        method='GET',
        url=f'http://test.local/products/{order_item.product_id}/stock',
        json={'stock': 3},
        status_code=200
    )

    stock_sufficient = await catalog_client.check_stock(product_id=order_item.product_id, quantity=order_item.quantity)

    assert not stock_sufficient


@pytest.mark.asyncio
async def test_check_stock_returns_false_if_product_not_found(catalog_client, order_item, httpx_mock):
    """Тестирование выполнения эндпоинта GET /products/{product_id}/stock при отсутствии требуемого товара"""
    httpx_mock.add_response(
        method='GET',
        url=f'http://test.local/products/{order_item.product_id}/stock',
        status_code=404
    )

    with pytest.raises(ProductNotFoundError):
        await catalog_client.check_stock(product_id=order_item.product_id, quantity=order_item.quantity)


@pytest.mark.asyncio
async def test_check_stock_raises_if_server_error(catalog_client, order_item, httpx_mock):
    """Тестирование выполнения эндпоинта GET /products/{product_id}/stock при ошибке сервера"""
    httpx_mock.add_response(
        method='GET',
        url=f'http://test.local/products/{order_item.product_id}/stock',
        status_code=500
    )

    with pytest.raises(CatalogUnavailableError):
        await catalog_client.check_stock(product_id=order_item.product_id, quantity=order_item.quantity)


@pytest.mark.asyncio
async def test_check_stock_raises_if_timeout(catalog_client, order_item, httpx_mock):
    """Тестирование выполнения эндпоинта GET /products/{product_id}/stock при таймауте"""
    httpx_mock.add_exception(
        method='GET',
        url=f'http://test.local/products/{order_item.product_id}/stock',
        exception=httpx.TimeoutException("Connection timed out"),
        is_reusable=True
    )

    with pytest.raises(CatalogUnavailableError):
        await catalog_client.check_stock(product_id=order_item.product_id, quantity=order_item.quantity)
