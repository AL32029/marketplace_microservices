from fastapi import Request


async def password_hasher_use_case_depends(request: Request):
    factory = request.app.state.services['password_hasher_repo']
    return await factory()
