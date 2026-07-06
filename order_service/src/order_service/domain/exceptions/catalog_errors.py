class CatalogServiceError(Exception):
    """Базовое исключение для ошибок Catalog Service"""
    pass

class CatalogUnavailableError(CatalogServiceError):
    """Catalog Service недоступен (таймаут, 5xx)"""
    pass

class ProductNotFoundError(CatalogServiceError):
    """Товар не найден в каталоге"""
    pass