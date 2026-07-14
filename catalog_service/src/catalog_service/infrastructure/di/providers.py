from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from catalog_service.application.ports.product_repo import ProductRepository
from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.application.services.get_stock import GetStockUseCase
from catalog_service.application.services.reserve_stock import ReserveStockUseCase
from catalog_service.infrastructure.config import DatabaseSettings
from catalog_service.infrastructure.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepo,
)


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_engine(self, settings: DatabaseSettings) -> AsyncEngine:
        engine = create_async_engine(
            settings.DB_URL.unicode_string(),
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )
        return engine

    @provide
    def provide_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
        )

    # Опционально: провайдер самой сессии (Scope.REQUEST)
    @provide
    async def provide_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
        async with session_maker() as session:
            yield session


class CatalogProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def db_product_repo(self, session: AsyncSession) -> ProductRepository:
        return SQLAlchemyProductRepo(session)

    @provide(scope=Scope.REQUEST)
    async def create_product_use_case(self, db_repo: ProductRepository) -> CreateProductUseCase:
        return CreateProductUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def all_products_use_case(self, db_repo: ProductRepository) -> GetAllProductsUseCase:
        return GetAllProductsUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def get_stock_use_case(self, db_repo: ProductRepository) -> GetStockUseCase:
        return GetStockUseCase(db_repo)

    @provide(scope=Scope.REQUEST)
    async def reserve_stock_use_case(self, db_repo: ProductRepository) -> ReserveStockUseCase:
        return ReserveStockUseCase(db_repo)
