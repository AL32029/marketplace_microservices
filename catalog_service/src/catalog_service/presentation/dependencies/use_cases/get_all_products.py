from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from catalog_service.application.services.get_all_products import GetAllProductsUseCase
from catalog_service.presentation.dependencies.db.get_db_session import get_db


async def get_all_products_use_case_depends(
        request: Request, session: AsyncSession = Depends(get_db)
) -> GetAllProductsUseCase:
    factory = request.app.state.services['get_all_products_use_case']
    return await factory(session)
