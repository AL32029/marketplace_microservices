from order_service.domain.entities.order import Order, OrderStatus, OrderItem
from order_service.infrastructure.db.models import OrderORM, OrderItemORM


def orm_to_domain(order_orm: OrderORM) -> Order:
    return Order(
        id=order_orm.id,
        user_id=order_orm.user_id,
        status=OrderStatus(order_orm.status),
        total=order_orm.total,
        items=[
            OrderItem(product_id=item.product_id, quantity=item.quantity, price=item.price)
            for item in order_orm.items
        ]
    )


def domain_to_orm(order: Order) -> OrderORM:
    return OrderORM(
        id=order.id,
        user_id=order.user_id,
        status=order.status.value,
        total=order.total,
        items=[
            OrderItemORM(product_id=item.product_id, quantity=item.quantity, price=item.price)
            for item in order.items
        ]
    )
