# order_service/src/order_service/infrastructure/db/models.py
import datetime
from typing import List, Optional

from sqlalchemy import Integer, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrderORM(Base):
    __tablename__ = 'orders'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32))
    total: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now)

    items: Mapped[List['OrderItemORM']] = relationship('OrderItemORM', back_populates='order', lazy='joined',
                                                       cascade='all, delete-orphan')


class OrderItemORM(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)

    order: Mapped['OrderORM'] = relationship('OrderORM', back_populates='items', lazy='joined')