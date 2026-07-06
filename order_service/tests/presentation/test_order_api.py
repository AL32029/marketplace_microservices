import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from order_service.main import app
from order_service.domain.entities.order import Order, OrderStatus, OrderItem

@pytest.mark.asyncio
async def test_create_order_endpoint():
    mock_use_case = AsyncMock()
    mock_use_case.execute.return_value = Order(
        id=1,
        user_id=1,
        items=[OrderItem(product_id=1, quantity=2, price=10.0)],
        status=OrderStatus.PENDING,
        total=20.0
    )

    async def mock_factory():
        return mock_use_case

    app.state.services["create_order_use_case"] = mock_factory

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

    # 5. Проверяем результат
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["items"]) == 1
    assert data["status"] == "pending"

    mock_use_case.execute.assert_called_once_with(
        user_id=1,
        items=[OrderItem(product_id=1, quantity=2, price=10.0)]
    )

    from order_service.bootstrap import build_services
    app.state.services["create_order_use_case"] = build_services(app.state.session_maker)["create_order_use_case"]