
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from fastapi.params import Query

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.domain.exceptions.catalog_errors import (
    InsufficientStockError,
    NegativeQuantityError,
    ProductNotFoundError,
)
from catalog_service.presentation.mappers.product_mappers import domain_to_response
from catalog_service.presentation.schemas.product_schemas import (
    CreateProductRequest,
    ProductResponse,
)

router = APIRouter(prefix='/products', tags=['Product Methods'])


@router.get('/{product_id}/stock', response_model=dict[str, int])
@inject
async def get_product_stock(use_case: FromDishka[GetStockUseCase], product_id: int) -> dict[str, int]:
    """Получение остатка товара"""
    try:
        stock = await use_case.get_stock(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return {'stock': stock}


@router.post('/{product_id}/reserve', response_model=dict[str, bool])
@inject
async def reserve_product_stock(
        use_case: FromDishka[ReserveStockUseCase],
        product_id: int,
        quantity: int = Query(ge=1),
) -> dict[str, bool]:
    """Резервирование товара"""
    try:
        await use_case.reserve_stock(product_id, quantity)
    except NegativeQuantityError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {'success': True}


@router.get('', response_model=list[ProductResponse])
@inject
async def get_all_products(use_case: FromDishka[GetAllProductsUseCase]) -> list[ProductResponse]:
    """Получение списка всех товаров"""
    products = await use_case.get_all_products()
    return [domain_to_response(product) for product in products]


@router.post('', response_model=ProductResponse)
@inject
async def add_new_product(use_case: FromDishka[CreateProductUseCase],
                          item_info: CreateProductRequest) -> ProductResponse:
    """Добавление нового товара"""
    item = await use_case.execute(item_info.name, item_info.price, item_info.stock)
    return domain_to_response(item)
