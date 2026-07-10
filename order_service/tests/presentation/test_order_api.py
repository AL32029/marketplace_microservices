import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from order_service.main import app
from order_service.domain.entities.order import Order, OrderStatus, OrderItem
from order_service.presentation.dependencies import create_order_use_case_depends


@pytest.mark.asyncio
async def test_create_order_endpoint():
    """Тестирование эндпоинта POST /orders/"""
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = Order(
        id=1,
        user_id=1,
        items=[OrderItem(product_id=1, quantity=2, price=10.0)],
        status=OrderStatus.PENDING,
        total=20.0
    )

    app.dependency_overrides[create_order_use_case_depends] = lambda: mock_use_case

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as client:
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

    mock_use_case.execute.assert_called_once_with(
        user_id=1,
        items=[OrderItem(product_id=1, quantity=2, price=10.0)]
    )

    app.dependency_overrides.clear()
