from user_service.domain.entities.user import User
from user_service.presentation.schemas.user_schema import UserProfileResponse


def domain_to_response(user_domain: User) -> UserProfileResponse:
    return UserProfileResponse(
        id=user_domain.id,
        email=user_domain.email.value,
        full_name=user_domain.full_name,
        role=user_domain.role
    )
