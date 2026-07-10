from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession


async def get_db(request: Request) -> AsyncSession:
    async with request.app.state.session_maker() as session:
        yield session
