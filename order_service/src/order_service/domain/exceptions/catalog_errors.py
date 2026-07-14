class OrderServiceError(Exception):
    """Базовое исключение для ошибок Order Service"""
    pass


class CatalogUnavailableError(OrderServiceError):
    """Catalog Service недоступен (таймаут, 5xx)"""
    pass


class ProductNotFoundError(OrderServiceError):
    """Товар не найден в каталоге"""
    pass


class OrderWasPayedError(OrderServiceError):
    """Ошибка попытки отмены оплаченного заказа"""
    pass
