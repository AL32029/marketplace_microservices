import asyncio

import httpx
from httpx import HTTPStatusError, TimeoutException

from order_service.application.ports.catalog_repo import CatalogClient
from order_service.domain.exceptions.catalog_errors import (
    CatalogUnavailableError,
    ProductNotFoundError,
)


class HTTPCatalogClient(CatalogClient):
    def __init__(self, base_url: str, timeout: int = 5, retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries

    async def check_stock(self, product_id: int, quantity: int) -> bool:
        url = f"{self.base_url}/products/{product_id}/stock"

        for attempt in range(self.retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url)
                    response.raise_for_status()

                    data = response.json()
                    stock = data.get("stock", 0)
                    return stock >= quantity

            except HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise ProductNotFoundError(f"Product {product_id} not found") from e
                raise CatalogUnavailableError(f"Catalog service error: {e.response.status_code}") from e

            except TimeoutException as e:
                if attempt < self.retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise CatalogUnavailableError(f"Catalog service timeout after {self.retries} attempts") from e

            except Exception as e:
                raise CatalogUnavailableError(f"Unexpected catalog error: {str(e)}") from e

        raise CatalogUnavailableError("Catalog service unavailable after retries")