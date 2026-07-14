from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.domain.exceptions.catalog_errors import ProductNotFoundError, CatalogUnavailableError
from order_service.presentation.mappers.order_mappers import request_to_domain, domain_to_response
from order_service.presentation.schemas.order_schemas import OrderResponse, CreateOrderRequest

router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('/', response_model=OrderResponse)
@inject
async def create_order(user_case: FromDishka[CreateOrderUseCase], request: CreateOrderRequest):
    try:
        user_id, items = request_to_domain(request)
        order = await user_case.execute(user_id=user_id, items=items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CatalogUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))

    return domain_to_response(order)