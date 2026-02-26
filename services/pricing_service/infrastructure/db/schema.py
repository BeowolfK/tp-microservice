import os
import uuid
from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/pricing_db",
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class PricingModel(Base):
    __tablename__ = "pricings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_pk: Mapped[str] = mapped_column(String(36), unique=True)
    price: Mapped[float] = mapped_column(Float)

    def __repr__(self) -> str:
        return f"PricingModel(id={self.id}, product_pk={self.product_pk!r}, price={self.price})"
