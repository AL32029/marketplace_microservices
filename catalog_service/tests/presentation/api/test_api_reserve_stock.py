import pytest


@pytest.mark.asyncio
async def test_reserve_stock_error_not_found(client):
    response = await client.post(
        '/products/50/reserve',
        params={'quantity': 50}
    )

    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert 'Product with ID 50 not found' in data['detail']
