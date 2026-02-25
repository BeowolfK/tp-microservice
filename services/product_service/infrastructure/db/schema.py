"""Schema SQLAlchemy pour le service Product."""

import os
import uuid
from sqlalchemy import create_engine, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/product_db",
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """Classe de base SQLAlchemy."""


class ProductModel(Base):
    """Modele SQLAlchemy representant un produit en base de donnees."""

    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000), default="")
    category: Mapped[str] = mapped_column(String(50))
    available: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        """Representation textuelle du modele."""
        return f"ProductModel(id={self.id}, name={self.name!r})"
