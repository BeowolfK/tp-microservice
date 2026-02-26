import os
import uuid
from sqlalchemy import create_engine, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db",
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class WarehouseModel(Base):
    __tablename__ = "warehouses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(200), default="")

    inventory_items = relationship("InventoryModel", back_populates="warehouse")

    def __repr__(self) -> str:
        return f"WarehouseModel(id={self.id}, name={self.name!r})"


class InventoryModel(Base):
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_pk: Mapped[str] = mapped_column(String(36))
    warehouse_pk: Mapped[str] = mapped_column(String(36), ForeignKey("warehouses.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    warehouse = relationship("WarehouseModel", back_populates="inventory_items")

    def __repr__(self) -> str:
        return f"InventoryModel(id={self.id}, product_pk={self.product_pk}, warehouse_pk={self.warehouse_pk}, quantity={self.quantity})"
