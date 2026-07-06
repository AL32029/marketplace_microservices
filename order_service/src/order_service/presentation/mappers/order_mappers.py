from order_service.domain.entities.order import OrderItem, Order
from order_service.presentation.schemas.order_schemas import CreateOrderRequest, OrderResponse, OrderItemResponse


def request_to_domain(request: CreateOrderRequest) -> tuple[int, list[OrderItem]]:
    items = [
        OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        for item in request.items
    ]
    return request.user_id, items


def domain_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        items=[
            OrderItemResponse(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            )
            for item in order.items
        ],
        status=order.status.value,
        total=order.total
    )
