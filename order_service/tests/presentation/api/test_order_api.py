import pytest
from dishka import Scope

from order_service.application.services.create_order import CreateOrderUseCase


@pytest.fixture(scope='function')
async def create_order_use_case(test_container) -> CreateOrderUseCase:
    async with test_container(scope=Scope.REQUEST) as request_container:
        return await request_container.get(CreateOrderUseCase)


@pytest.mark.asyncio
async def test_create_order_endpoint(create_order_use_case, client):
    """Тестирование эндпоинта POST /orders/"""
    response = await client.post(
        "/orders/",
        json={
            "user_id": 1,
            "items": [
                {"product_id": 1, "quantity": 2, "price": 10.0}
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["items"]) == 1
    assert data["status"] == "pending"
