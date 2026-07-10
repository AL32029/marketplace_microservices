from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.presentation.dependencies import get_db


async def create_order_use_case_depends(
        request: Request,
        session: AsyncSession = Depends(get_db)
):
    factory = request.app.state.services['create_order_use_case']
    return await factory(session)
