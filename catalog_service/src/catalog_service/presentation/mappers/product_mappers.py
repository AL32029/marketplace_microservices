from catalog_service.domain.entities.product import Product
from catalog_service.presentation.schemas.product_schemas import (
    CreateProductRequest,
    ProductResponse,
)


def request_to_domain(request: CreateProductRequest) -> Product:
    product = Product(
        name=request.name,
        price=request.price
    )

    return product


def domain_to_response(domain: Product) -> ProductResponse:
    product = ProductResponse(
        id=domain.id,
        name=domain.name,
        price=domain.price,
        stock=domain.stock
    )

    return product
