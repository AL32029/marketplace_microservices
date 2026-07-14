import pytest


@pytest.mark.asyncio
async def test_get_product_stock_error_not_found(client):
    response = await client.get(
        '/products/50/stock'
    )

    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'Product with ID 50 not found' in data['detail']
