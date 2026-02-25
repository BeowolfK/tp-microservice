import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/order_db",
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_pk: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    lines: Mapped[list["OrderLineModel"]] = relationship("OrderLineModel", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"OrderModel(id={self.id}, customer_pk={self.customer_pk!r}, status={self.status!r})"


class OrderLineModel(Base):
    __tablename__ = "order_lines"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_pk: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"))
    product_pk: Mapped[str] = mapped_column(String(36))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)

    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="lines")

    def __repr__(self) -> str:
        return f"OrderLineModel(id={self.id}, order_pk={self.order_pk!r}, product_pk={self.product_pk!r})"
