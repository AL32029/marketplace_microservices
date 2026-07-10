from user_service.application.ports.token_generator import TokenGeneratorRepo


class GetJWTSubUseCase:
    def __init__(self, repo: TokenGeneratorRepo):
        self.repo = repo

    def get_jwt_sub(self, token: str):
        sub = self.repo.decode_token(token)
