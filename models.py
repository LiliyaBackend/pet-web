from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    advertising: Mapped[bool]


class MathItem(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    desc: Mapped[str] = mapped_column(name="description")
    parameterized: Mapped[int]


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    count: Mapped[int]
    price: Mapped[int]

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    item: Mapped["MathItem"] = relationship("MathItem", backref="item_id")

class Order(Base):
    __tablename__ = "orders"

    order_number:Mapped[int] = mapped_column(name = "id", primary_key=True, autoincrement=True)
    userId: Mapped[str] = mapped_column(name = "user")
    card: Mapped[str]
    address: Mapped[str] = mapped_column(name = "addr")
    created: Mapped[str]

    items: Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all")

    def get_total(self):
        total = 0
        for item in self.items:
            total = total + item.price
        return total