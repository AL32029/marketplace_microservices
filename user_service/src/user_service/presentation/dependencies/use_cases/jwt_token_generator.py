from fastapi import Request

from user_service.infrastructure.repositories.jwt_token_generator import JWTTokenGeneratorRepo


async def jwt_token_generator_repo_depends(request: Request) -> JWTTokenGeneratorRepo:
    factory = request.app.state.services['jwt_token_generator_repo']
    return await factory(request.app.state.jwt_secret_key, request.app.state.jwt_algorithm)
