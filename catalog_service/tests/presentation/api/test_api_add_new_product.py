import pytest


@pytest.mark.asyncio
async def test_add_new_item(client):
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
async def test_add_new_item_validation_error(client, name, price, stock):
    response = await client.post(
        '/products',
        json={'name': name, 'price': price, 'stock': stock}
    )

    assert response.status_code == 422
