import pytest

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.tests.conftest import product_repo


@pytest.fixture
async def create_product_use_case(product_repo):
    return CreateProductUseCase(product_repo)
