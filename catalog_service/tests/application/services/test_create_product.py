from unittest.mock import AsyncMock

import pytest

from catalog_service.application.services.create_product import CreateProductUseCase


@pytest.mark.asyncio
async def test_create_product():
    """CreateProductUseCase должен создать продукт и сохранить его через репозиторий"""
    mock_repo = AsyncMock()
    mock_repo.save = AsyncMock()

    use_case = CreateProductUseCase(mock_repo)

    await use_case.execute(name='Вода дистиллированная', price=50)

    mock_repo.save.assert_called_once()
    saved = mock_repo.save.call_args[0][0]

    assert saved.name == 'Вода дистиллированная'
    assert saved.price == 50
    assert saved.stock == 0
