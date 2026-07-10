from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query

from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.domain.exceptions.catalog_errors import ProductNotFoundError, InsufficientStockError, \
    NegativeQuantityError
from catalog_service.presentation.dependencies import (
    get_stock_use_case_depends, reserve_stock_use_case_depends,
    get_all_products_use_case_depends, create_product_use_case_depends
)
from catalog_service.presentation.mappers.product_mappers import domain_to_response
from catalog_service.presentation.schemas.product_schemas import CreateProductRequest, ProductResponse

router = APIRouter(prefix='/products', tags=['Product Methods'])


@router.get('/{product_id}/stock')
async def get_product_stock(product_id: int, use_case: GetStockUseCase = Depends(get_stock_use_case_depends)):
    """Получение остатка товара"""
    try:
        stock = await use_case.get_stock(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {'stock': stock}


@router.post('/{product_id}/reserve')
async def reserve_product_stock(
        product_id: int,
        quantity: int = Query(ge=1),
        use_case: ReserveStockUseCase = Depends(reserve_stock_use_case_depends)
):
    """Резервирование товара"""
    try:
        await use_case.reserve_stock(product_id, quantity)
    except NegativeQuantityError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'success': True}


@router.get('')
async def get_all_products(use_case=Depends(get_all_products_use_case_depends)) -> List[ProductResponse]:
    """Получение списка всех товаров"""
    products = await use_case.get_all_products()
    return [domain_to_response(product) for product in products]


@router.post('')
async def add_new_product(
        item_info: CreateProductRequest, use_case=Depends(create_product_use_case_depends)
) -> ProductResponse:
    """Добавление нового товара"""
    item = await use_case.execute(item_info.name, item_info.price, item_info.stock)
    return domain_to_response(item)
