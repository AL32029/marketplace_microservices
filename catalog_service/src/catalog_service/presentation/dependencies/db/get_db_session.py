from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db(request: Request) -> AsyncSession:
    async with request.app.state.session_maker() as session:
        yield session
