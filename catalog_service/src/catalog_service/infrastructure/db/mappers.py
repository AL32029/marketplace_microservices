from catalog_service.domain.entities.product import Product
from catalog_service.infrastructure.db.models import ProductORM


def orm_to_domain(product_orm: ProductORM) -> Product:
    domain = Product(
        id=product_orm.id,
        name=product_orm.name,
        price=product_orm.price,
        stock=product_orm.stock
    )

    return domain


def domain_to_orm(domain: Product) -> ProductORM:
    product_orm = ProductORM(
        id=domain.id,
        name=domain.name,
        price=domain.price,
        stock=domain.stock
    )

    return product_orm
