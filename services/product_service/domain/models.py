from uuid import UUID, uuid4
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class Category(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    price: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(ge=0)
    category: Category
    available: bool = True

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("le nom ne peut pas etre vide")
        return v.strip()

    @field_validator("price", mode="before")
    @classmethod
    def price_rounded(cls, v) -> Decimal:
        return round(Decimal(str(v)), 2)


laptop = Product(
    name="MacBook Pro 14",
    description="Laptop Apple avec puce M3, 16Go RAM, 512Go SSD",
    price="1999.99",
    stock=42,
    category=Category.ELECTRONICS,
)
