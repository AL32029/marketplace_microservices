import pytest


@pytest.mark.asyncio
async def test_create_order_endpoint(httpx_mock, client):
    """Тестирование эндпоинта POST /orders/"""

    httpx_mock.add_response(
        url='http://test.local/products/1/stock',
        method='GET',
        json={
            'stock': 500
        },
        status_code=200
    )

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
