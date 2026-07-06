from fastapi import APIRouter, Depends, HTTPException, Request

from order_service.application.services.create_order import CreateOrderUseCase
from order_service.domain.exceptions.catalog_errors import ProductNotFoundError, CatalogUnavailableError
from order_service.presentation.mappers.order_mappers import request_to_domain, domain_to_response
from order_service.presentation.schemas.order_schemas import OrderResponse, CreateOrderRequest

router = APIRouter(prefix='/orders', tags=['Orders'])

async def get_use_case(request: Request) -> CreateOrderUseCase:
    # Достаём фабрику из состояния и вызываем её (она создаст сессию)
    factory = request.app.state.services["create_order_use_case"]
    return await factory()

@router.post('/', response_model=OrderResponse)
async def create_order(
        request: CreateOrderRequest,
        user_case: CreateOrderUseCase = Depends(get_use_case)
):
    try:
        user_id, items = request_to_domain(request)
        order = await user_case.execute(user_id=user_id, items=items)
        return domain_to_response(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except CatalogUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))