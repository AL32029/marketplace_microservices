from user_service.domain.entities.user import User
from user_service.domain.value_objects.email import Email
from user_service.domain.value_objects.password import Password
from user_service.infrastructure.db.models import UserORM


def domain_to_orm(user: User) -> UserORM:
    return UserORM(
        id=user.id,
        email=user.email.value,
        full_name=user.full_name,
        password_hash=user.password_hash.value,
        role=user.role,
        created_at=user.created_at,
    )


def orm_to_domain(user_orm: UserORM) -> User:
    return User(
        id=user_orm.id,
        email=Email(user_orm.email),
        full_name=user_orm.full_name,
        password_hash=Password(user_orm.password_hash),
        role=user_orm.role,
        created_at=user_orm.created_at,
    )
