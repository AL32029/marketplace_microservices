# TODO: Покрыть исключения кастомными ошибками
class CatalogServiceError(Exception):
    """Базовое исключение для ошибок Catalog Service"""
    pass


class CatalogUnavailableError(CatalogServiceError):
    """Catalog Service недоступен (таймаут, 5xx)"""
    pass


class ProductNotFoundError(CatalogServiceError):
    """Товар не найден в каталоге"""
    pass


class InsufficientStockError(CatalogServiceError):
    """Ошибка запасов товара"""
    pass


class NegativeQuantityError(CatalogServiceError):
    """Ошибка ввода отрицательного числа в количестве"""
    pass
