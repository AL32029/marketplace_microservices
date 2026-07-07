from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from catalog_service.application.services.create_product import CreateProductUseCase
from catalog_service.presentation.dependencies.db.get_db_session import get_db


async def create_product_use_case_depends(
        request: Request, session: AsyncSession = Depends(get_db)
) -> CreateProductUseCase:
    factory = request.app.state.services['create_product_use_case']
    return await factory(session)
